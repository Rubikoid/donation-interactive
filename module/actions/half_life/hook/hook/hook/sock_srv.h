#pragma once

#include "pch.h"
#include <winsock2.h>

class TCPSrv
{
public:
    SOCKET lSock;
    WSAData wData;

    TCPSrv();
    ~TCPSrv();
    int start();
    void stop();
    void handle();
};
