from socket import *
import sys

serversocket = socket(AF_INET, SOCK_STREAM)
serverport = 6789
serversocket.bind(("localhost",serverport))
serversocket.listen(1)
while True:
    print("siap")
    ConnectionSocket, addr = serversocket.accept()
    try:
        message = ConnectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        ConnectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        for i in range(0, len(outputdata)):
            ConnectionSocket.send(outputdata[i].encode())
        ConnectionSocket.send("\r\n".encode())
        ConnectionSocket.close()
    except IOError:
        ConnectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        ConnectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        ConnectionSocket.close()