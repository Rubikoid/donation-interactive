// pch.h: This is a precompiled header file.
// Files listed below are compiled only once, improving build performance for future builds.
// This also affects IntelliSense performance, including code completion and many code browsing features.
// However, files listed here are ALL re-compiled if any one of them is updated between builds.
// Do not add files here that you will be updating frequently as this negates the performance advantage.

#ifndef PCH_H
#define PCH_H

// add headers that you want to pre-compile here
#include "framework.h"
#include "magic_header.h"
#include "second_magic_header.h"
#include "Engine.h"
#include "sock_srv.h"

#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <stdio.h>

extern FILE* _log;

#define LOG_PATH "C:\\Users\\isika\\Desktop\\Log\\log.txt"
#define dolog(x, ...) fopen_s(&_log, LOG_PATH, "a"); fprintf(_log, x, __VA_ARGS__); fclose(_log);

#endif //PCH_H
