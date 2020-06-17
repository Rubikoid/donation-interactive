// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
FILE* _log = 0;

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
    g_Engine.pfnClientCmd((char*)"echo WE ARE HOOKED INTO HL!");

    dolog("[SetupHook] I think, we hooked into the game?\n");

    TCPSrv srv = TCPSrv();
    if (!srv.start()) {
        srv.handle();
    }
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

