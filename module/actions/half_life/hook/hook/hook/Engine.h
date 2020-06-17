#pragma once

#include "magic_header.h"

extern BYTE HLType;
extern DWORD HwBase, HwSize, HwEnd;
extern DWORD ClBase, ClSize, ClEnd;
extern DWORD HlBase, HlSize, HlEnd;
extern cl_clientfunc_t* g_pClient;
extern cl_enginefunc_t* g_pEngine;

extern cl_enginefunc_t g_Engine;

DWORD FarProc(const DWORD Address, DWORD LB, DWORD HB);
BOOL __comparemem(const UCHAR* buff1, const UCHAR* buff2, UINT size);
ULONG __findmemoryclone(const ULONG start, const ULONG end, const ULONG clone, UINT size);
ULONG __findreference(const ULONG start, const ULONG end, const ULONG address);
DWORD GetModuleSize(const DWORD Address);
bool GetRendererInfo();
PVOID ClientFuncsOffset();
PVOID EngineFuncsOffset();
