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
