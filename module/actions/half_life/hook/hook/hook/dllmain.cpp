// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"

FILE* _log = 0;
#define dolog(x, ...) fopen_s(&_log, "D:\\Dsct\\Progs\\donation-interactive\\module\\actions\\half_life\\log.txt", "a"); fprintf(_log, x, __VA_ARGS__); fclose(_log);

#define RENDERTYPE_UNDEFINED	0
#define RENDERTYPE_SOFTWARE		1
#define RENDERTYPE_HARDWARE		2
#define RENDERTYPE_D3D			3

#define CompareMemory(Buff1, Buff2, Size) __comparemem((const UCHAR *)Buff1, (const UCHAR *)Buff2, (UINT)Size)
#define FindMemoryClone(Start, End, Clone, Size) __findmemoryclone((const ULONG)Start, (const ULONG)End, (const ULONG)Clone, (UINT)Size)
#define FindReference(Start, End, Address) __findreference((const ULONG)Start, (const ULONG)End, (const ULONG)Address)

BYTE HLType;
DWORD HwBase, HwSize, HwEnd;
DWORD ClBase, ClSize, ClEnd;
DWORD HlBase, HlSize, HlEnd;
cl_clientfunc_t* g_pClient = NULL;
cl_enginefunc_t* g_pEngine = NULL;

cl_enginefunc_t g_Engine;

DWORD FarProc(const DWORD Address, DWORD LB, DWORD HB)
{
    return ((Address < LB) || (Address > HB));
}

BOOL __comparemem(const UCHAR* buff1, const UCHAR* buff2, UINT size)
{
    for (UINT i = 0; i < size; i++, buff1++, buff2++)
    {
        if ((*buff1 != *buff2) && (*buff2 != 0xFF))
            return FALSE;
    }
    return TRUE;
}

ULONG __findmemoryclone(const ULONG start, const ULONG end, const ULONG clone, UINT size)
{
    for (ULONG ul = start; (ul + size) < end; ul++)
    {
        if (CompareMemory(ul, clone, size))
            return ul;
    }
    return NULL;
}

ULONG __findreference(const ULONG start, const ULONG end, const ULONG address)
{
    UCHAR Pattern[5];
    Pattern[0] = 0x68;
    *(ULONG*)&Pattern[1] = address;
    return FindMemoryClone(start, end, Pattern, sizeof(Pattern) - 1);
}

DWORD GetModuleSize(const DWORD Address)
{
    return PIMAGE_NT_HEADERS(Address + (DWORD)PIMAGE_DOS_HEADER(Address)->e_lfanew)->OptionalHeader.SizeOfImage;
}

bool GetRendererInfo() {
    DWORD GameUI = (DWORD)GetModuleHandle(L"GameUI.dll");
    DWORD vgui = (DWORD)GetModuleHandle(L"vgui.dll");
    DWORD vgui2 = (DWORD)GetModuleHandle(L"vgui2.dll");
    DWORD d3dim = (DWORD)GetModuleHandle(L"d3dim.dll");

    HwBase = (DWORD)GetModuleHandle(L"hw.dll"); // Hardware

    if (HwBase == NULL)
    {
        HwBase = (DWORD)GetModuleHandle(L"sw.dll"); // Software
        if (HwBase == NULL)
        {
            HwBase = (DWORD)GetModuleHandle(NULL); // Non-Steam?
            if (HwBase == NULL) // Invalid module handle.
            {
                dolog("Invalid module handle.\n");
                ExitProcess(0);
            }
            else
                HLType = RENDERTYPE_UNDEFINED;
        }
        else
            HLType = RENDERTYPE_SOFTWARE;
    }
    else
    {
        if (d3dim == NULL)
            HLType = RENDERTYPE_HARDWARE;
        else
            HLType = RENDERTYPE_D3D;
    }

    HwSize = (DWORD)GetModuleSize(HwBase);

    if (HwSize == NULL)
    {
        switch (HwSize)
        {
        case RENDERTYPE_HARDWARE: HwSize = 0x122A000; break;
        case RENDERTYPE_UNDEFINED: HwSize = 0x2116000; break;
        case RENDERTYPE_SOFTWARE: HwSize = 0xB53000; break;
        default: {dolog("Invalid renderer type.\n"); ExitProcess(0); }
        }
    }

    HwEnd = HwBase + HwSize - 1;

    ClBase = (DWORD)GetModuleHandle(L"client.dll");

    if (ClBase != NULL) {
        ClSize = (DWORD)GetModuleSize(ClBase);
        ClEnd = ClBase + ClSize - 1;
    }
    else {
        ClBase = HwBase;
        ClEnd = HwEnd;
        ClSize = HwSize;
    }

    /*if (GameUI != NULL)
    {
        UiBase = GameUI;
        UiSize = (DWORD)GetModuleSize(UiBase);
        UiEnd = UiBase + UiSize - 1;
    }*/

    HlBase = (DWORD)GetModuleHandle(NULL);
    HlSize = (DWORD)GetModuleSize(HlBase);
    HlEnd = HlBase + HlSize - 1;

    return (HwBase && ClBase && GameUI && vgui && vgui2 && HlBase);
}

PVOID ClientFuncsOffset()
{
    DWORD Old = NULL;
    const char* String = "ScreenFade";
    DWORD Address = (DWORD)FindMemoryClone(HwBase, HwEnd, String, strlen(String));
    ULONG reference = FindReference(HwBase, HwEnd, Address);
    PVOID ClientPtr = (PVOID) * (PDWORD)(reference + 0x13); // all patch

    dolog("[ClientFuncsOffset] Found addres of screenfade=%x, reference=%x, clientptr=%x\n", Address, reference, (UINT)ClientPtr);

    if (FarProc((DWORD)ClientPtr, HwBase, HwEnd)) {
        dolog("Couldn't find ClientPtr pointer.\n");
        ExitProcess(0);
    }
    //Error("Couldn't find ClientPtr pointer.");

    VirtualProtect(ClientPtr, sizeof(double), PAGE_READWRITE, &Old);

    return ClientPtr;
}

PVOID EngineFuncsOffset()
{
    DWORD Old = NULL;
    PVOID EnginePtr = (cl_enginefunc_t*)*(DWORD*)((DWORD)g_pClient->Initialize + 0x22); // old patch
    dolog("[EngineFuncsOffset] Basic addr=%x\n", (DWORD)g_pClient->Initialize);
    if (FarProc((DWORD)EnginePtr, HwBase, HwEnd) && FarProc((DWORD)EnginePtr, HlBase, HlEnd))
    {
        dolog("[EngineFuncsOffset] Not old patch, addr=%x\n", (UINT)EnginePtr);
        EnginePtr = (cl_enginefunc_t*)*(DWORD*)((DWORD)g_pClient->Initialize + 0x1C); // new patch
        if (FarProc((DWORD)EnginePtr, ClBase, ClEnd))
        {
            dolog("[EngineFuncsOffset] Not new patch, addr=%x\n", (UINT)EnginePtr);
            EnginePtr = (cl_enginefunc_t*)*(DWORD*)((DWORD)g_pClient->Initialize + 0x1D); // steam
            if (FarProc((DWORD)EnginePtr, ClBase, ClEnd))
            {
                dolog("[EngineFuncsOffset] Not steam, addr=%x\n", (UINT)EnginePtr);
                EnginePtr = (cl_enginefunc_t*)*(DWORD*)((DWORD)g_pClient->Initialize + 0x37); // hl-steam
                if (FarProc((DWORD)EnginePtr, ClBase, ClEnd))
                {
                    dolog("[EngineFuncsOffset] Not hl-team, addr=%x\n", (UINT)EnginePtr);
                    EnginePtr = (cl_enginefunc_t*)*(DWORD*)((DWORD)g_pClient->Initialize + 0x12 + 1); // sven-coop
                    if (FarProc((DWORD)EnginePtr, ClBase, ClEnd))
                    {
                        dolog("[EngineFuncsOffset] Couldn't find EnginePtr pointer, addr=%x\n", (UINT)EnginePtr);
                        __debugbreak();
                        ExitProcess(0);
                    }
                }
            }
        }
    }
    dolog("[EngineFuncsOffset] Found addres of EnginePtr=%x\n", (UINT)EnginePtr);
    VirtualProtect(EnginePtr, sizeof(double), PAGE_READWRITE, &Old);
    return EnginePtr;
}

void SetupHook() {
    dolog("[SetupHook] Start hooking?\n");
    while (!GetRendererInfo())
        Sleep(100);
    dolog("[SetupHook] RendererInfo ok, type=%x!\n", HLType);
    dolog("[SetupHook] RendererInfo: hwbase=%x,hwend=%x\n", HwBase, HwEnd);
    dolog("[SetupHook] RendererInfo: clbase=%x,clend=%x\n", ClBase, ClEnd);
    g_pClient = (cl_clientfunc_t*)ClientFuncsOffset();
    dolog("[SetupHook] Client offset ok = %x\n", (UINT)g_pClient);
    g_pEngine = (cl_enginefunc_t*)EngineFuncsOffset();
    dolog("[SetupHook] Maybe we has been hooked...?\n");
    dolog("[SetupHook] Loading result: engine=%x.\n", (UINT)g_pEngine);

    while (!g_Engine.V_CalcShake)
        RtlCopyMemory(&g_Engine, g_pEngine, sizeof(cl_enginefunc_t));

    g_Engine.pfnClientCmd((char*)"echo HEEEY, THIS SHIT WORKS");
    g_Engine.pfnClientCmd((char*)"echo WE ARE HOOKED INTO CS 1.6");

    dolog("[SetupHook] I think, we hooked into the game?\n");
    // g_pEngine = (cl_enginefunc_t*)EngineFuncs();

}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {

    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        dolog("\n\nHooked!\n");
        DisableThreadLibraryCalls(hModule);
        CreateThread(0, 0, (LPTHREAD_START_ROUTINE)SetupHook, 0, 0, 0);
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

