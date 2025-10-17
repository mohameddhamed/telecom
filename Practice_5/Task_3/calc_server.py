from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct

server_addr = ("", 10000)
unpacker = struct.Struct("I I 1s")  # int, int, char[1]

with socket(AF_INET, SOCK_STREAM) as server:
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1.0)

    while True:
        try:
            client, client_addr = server.accept()
            print("Connected:", client_addr)

            data = client.recv(unpacker.size)
            print("Receieved:", data)

            unp_data = unpacker.unpack(data)
            print("Unpack:", unp_data)

            x = eval(str(unp_data[0]) + unp_data[2].decode() + str(unp_data[1]))

            client.sendall(str(x).encode())

        except timeout:
            pass
