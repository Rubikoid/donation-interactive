#include <windows.h>
#include <stdio.h>
#include <Libloaderapi.h>

int main()
{
    HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
    FARPROC ptr = GetProcAddress(kernel32, "LoadLibraryW");
    printf("%x\n", ptr);
}
