import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# https://docs.microsoft.com/ru-ru/windows/win32/inputdev/virtual-key-codes
VIRTUAL_KEYS = {'RETURN': 0x0D,
                'CTRL': 0x11,
                'SHIFT': 0x10,
                'MENU': 0x12,
                'TAB': 0x09,
                'BACKSPACE': 0x08,
                'CLEAR': 0x0C,
                'CAPSLOCK': 0x14,
                'ESCAPE': 0x1B,
                'HOME': 0x24,
                'INS': 0x2D,
                'DEL': 0x2E,
                'END': 0x23,
                'PRINTSCREEN': 0x2C,
                'CANCEL': 0x03,
                'BACK': 0x08,
                'LBUTTON': 0x01,
                'SPACE': 0x20,
                'LSHIFT': 0xA0,
                'RSHIFT': 0xA1,
                'LCTRL': 0xA2,
                'RCTRL': 0xA3
}

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions
def PressKey(hexKeyCode):
    #print(f"Pressed {hexKeyCode}")
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    #print(f"Released {hexKeyCode}")
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def PressAndRelease(key, duration=0.1):
    kbdctypes.ReleaseAll()
    if type(key) == str:
        if key in VIRTUAL_KEYS.keys():
            key = VIRTUAL_KEYS[key]
        else:
            key = ord(key.upper())
    PressKey(key)
    time.sleep(duration)
    ReleaseKey(key)


def ReleaseAll():
    for i in range(256):
        ReleaseKey(i)


def BlockInput(flag):
    user32.BlockInput(flag)
