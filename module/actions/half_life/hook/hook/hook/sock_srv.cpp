#include "pch.h"
#pragma comment (lib, "Ws2_32.lib")

#define socket_check_cleanup(sock, check, msg, free, free1) \
    if (sock == check) { dolog(msg" failed with error: %ld\n", WSAGetLastError()); \
        free; \
        free1; \
        WSACleanup(); \
        return 1; \
    }

TCPSrv::TCPSrv() {
    lSock = NULL;
}

TCPSrv::~TCPSrv() {
}

int TCPSrv::start() {
    int iResult;

    struct addrinfo* result = NULL;
    struct addrinfo hints;

    iResult = WSAStartup(MAKEWORD(2, 2), &wData);
    if (iResult != 0) {
        dolog("[TCPSRV] WSAStartup failed with error: %d\n", iResult);
        return 1;
    }

    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    iResult = getaddrinfo("127.0.0.1", "9998", &hints, &result);
    if (iResult != 0) {
        dolog("[TCPSRV] getaddrinfo failed with error: %d\n", iResult);
        WSACleanup();
        return 1;
    }

    lSock = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
    socket_check_cleanup(lSock, INVALID_SOCKET, "[TCPSRV] socket", freeaddrinfo(result), ;);

    // Setup the TCP listening socket
    iResult = bind(lSock, result->ai_addr, (int)result->ai_addrlen);
    socket_check_cleanup(iResult, SOCKET_ERROR, "[TCPSRV] bind", freeaddrinfo(result), closesocket(lSock));
    freeaddrinfo(result);

    iResult = listen(lSock, SOMAXCONN);
    socket_check_cleanup(iResult, SOCKET_ERROR, "[TCPSRV] listen", closesocket(lSock), ;);

    dolog("[TCPSRV] Ok started\n");
    return 0;
    /*
    // Receive until the peer shuts down the connection
    do {

        iResult = recv(ClientSocket, recvbuf, recvbuflen, 0);
        if (iResult > 0) {
            dolog("Bytes received: %d\n", iResult);

            // Echo the buffer back to the sender
            iSendResult = send(ClientSocket, recvbuf, iResult, 0);
            if (iSendResult == SOCKET_ERROR) {
                dolog("send failed with error: %d\n", WSAGetLastError());
                closesocket(ClientSocket);
                WSACleanup();
                return 1;
            }
            dolog("Bytes sent: %d\n", iSendResult);
        }
        else if (iResult == 0) {
            dolog("Connection closing...\n");
        }
        else {
            dolog("recv failed with error: %d\n", WSAGetLastError());
            closesocket(ClientSocket);
            WSACleanup();
            return 1;
        }

    } while (iResult > 0);
    */
    // return 0;
    /*
    if (WSAStartup(MAKEWORD(2, 2), &wData) == 0)
    {
        printf("WSA Startup succes\n");
    }
    SOCKADDR_IN addr;
    int addrl = sizeof(addr);
    addr.sin_addr.S_un.S_addr = INADDR_ANY;
    addr.sin_port = htons(port);
    addr.sin_family = AF_INET;
    this_s = socket(AF_INET, SOCK_STREAM, NULL);
    if (this_s == SOCKET_ERROR) {
        printf("Socket not created\n");
    }

    if (bind(this_s, (struct sockaddr*) & addr, sizeof(addr)) != SOCKET_ERROR) {
        printf("Socket succed binded\n");
    }

    if (listen(this_s, SOMAXCONN) != SOCKET_ERROR) {
        printf("Start listenin at port%u\n", ntohs(addr.sin_port));
    }
    handle();*/
}

void TCPSrv::stop() {
    closesocket(lSock);
    WSACleanup();
    dolog("Server stopped\n");
}

void TCPSrv::handle() {
    int iResult = 0;
    char recvbuf[512 + 4];
    int recvbuflen = 512;
    dolog("[TCPSRV] Starting handle\n");
    while (true)
    {
        SOCKET cSock;
        SOCKADDR_IN addr_c;
        int addrlen = sizeof(addr_c);
        if ((cSock = accept(lSock, (struct sockaddr*) & addr_c, &addrlen)) != 0) {
            dolog("[TCPSRV] Client connected from :%u\n", ntohs(addr_c.sin_port));
            do {
                iResult = recv(cSock, recvbuf, recvbuflen, 0);
                if (iResult > 0) {
                    recvbuf[iResult] = '\0';
                    dolog("[TCPSRV] Recvd (%d bytes): '%s'\n", iResult, recvbuf);
                    g_Engine.pfnClientCmd(recvbuf);
                }
                else if (iResult == 0) {
                    dolog("[TCPSRV] Connection closing\n");
                    closesocket(cSock);
                    break;
                }
                else {
                    dolog("[TCPSRV] Recv failed with error: %d\n", WSAGetLastError());
                    closesocket(cSock);
                }
            } while (iResult > 0);
            //SClient* client = new SClient(acceptS, addr_c);

        }
        else {
            dolog("[TCPSRV] accept fail: %x\n", cSock);
        }
        Sleep(50);
    }
}
