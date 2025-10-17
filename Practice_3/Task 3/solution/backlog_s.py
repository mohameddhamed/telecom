from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout, error
import sys

server_addr = ("", int(sys.argv[1]))

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(0)

    while True:
        try:
            client, client_addr = server.accept()
            print("Connected:", client_addr)
            data = client.recv(256).decode()
            print("Received:", data)
            client.send("Hello Client!".encode())
            client.close()
        except error:
            pass
