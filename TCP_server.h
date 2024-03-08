#pragma once
#include <iostream>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define BUFFER_SIZE 1024

class TCPServer
{
private:
    SOCKET serverSock;

public:
    TCPServer()
    {
        // Initialize Winsock
        WSADATA wsaData;
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
        {
            std::cerr << "Failed to initialize Winsock\n";
            return;
        }

        // Create socket
        serverSock = socket(AF_INET, SOCK_STREAM, 0);
        if (serverSock == INVALID_SOCKET)
        {
            std::cerr << "Failed to create socket\n";
            WSACleanup();
            return;
        }
    }

    ~TCPServer()
    {
        closesocket(serverSock);
        WSACleanup();
    }

    bool start(int port)
    {
        // Configure server address
        struct sockaddr_in serverAddr;
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_addr.s_addr = INADDR_ANY;
        serverAddr.sin_port = htons(port);

        // Bind socket
        if (bind(serverSock, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR)
        {
            std::cerr << "Bind failed\n";
            return false;
        }

        // Listen for incoming connections
        listen(serverSock, 3);
        std::cout << "Waiting for incoming connections on port " << port << "...\n";
        return true;
    }

    SOCKET acceptClient()
    {
        struct sockaddr_in clientAddr;
        int clientAddrSize = sizeof(clientAddr);
        SOCKET clientSock = accept(serverSock, (struct sockaddr *)&clientAddr, &clientAddrSize);
        if (clientSock == INVALID_SOCKET)
        {
            std::cerr << "Accept failed\n";
            return INVALID_SOCKET;
        }
        std::cout << "Connection accepted\n";
        return clientSock;
    }

    bool receiveData(SOCKET clientSock, char *buffer, int bufferSize)
    {
        int recvSize = recv(clientSock, buffer, bufferSize, 0);
        if (recvSize > 0)
        {
            return true;
        }
        else if (recvSize == 0)
        {
            std::cout << "Client disconnected\n";
            return false;
        }
        else
        {
            std::cerr << "Receive failed\n";
            return false;
        }
    }

    bool sendData(SOCKET clientSock, const char *data, int dataSize)
    {
        if (send(clientSock, data, dataSize, 0) == SOCKET_ERROR)
        {
            std::cerr << "Send failed\n";
            return false;
        }
        return true;
    }
};
