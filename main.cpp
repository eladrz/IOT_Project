#include "TCP_server.h"
int main()
{
    TCPServer server;
    if (!server.start(8080))
    {
        std::cerr << "Failed to start server\n";
        return 1;
    }

    SOCKET clientSock = server.acceptClient();
    if (clientSock == INVALID_SOCKET)
    {
        return 1;
    }

    char buffer[BUFFER_SIZE];
    while (server.receiveData(clientSock, buffer, BUFFER_SIZE))
    {
        // Echo back received data
        server.sendData(clientSock, buffer, strlen(buffer));
    }

    return 0;
}
