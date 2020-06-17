#pragma once

#ifndef __cplusplus
typedef enum { false, true }	qboolean;
#else
typedef int qboolean;
#endif

typedef unsigned char byte;
typedef unsigned short word;
typedef float vec_t;
typedef int (*pfnUserMsgHook)(const char* pszName, int iSize, void* pbuf);
typedef int HSPRITE_t;

typedef struct rect_s
{
    int				left, right, top, bottom;
} wrect_t;

class Vector {
public:
    float x, y, z;
};

#define vec3_t Vector


#define RENDERTYPE_UNDEFINED	0
#define RENDERTYPE_SOFTWARE		1
#define RENDERTYPE_HARDWARE		2
#define RENDERTYPE_D3D			3

#define CompareMemory(Buff1, Buff2, Size) __comparemem((const UCHAR *)Buff1, (const UCHAR *)Buff2, (UINT)Size)
#define FindMemoryClone(Start, End, Clone, Size) __findmemoryclone((const ULONG)Start, (const ULONG)End, (const ULONG)Clone, (UINT)Size)
#define FindReference(Start, End, Address) __findreference((const ULONG)Start, (const ULONG)End, (const ULONG)Address)
