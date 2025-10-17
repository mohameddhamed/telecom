from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct

server_addr = ('', 10000)
unpacker = struct.Struct('I I 1s')  # int, int, char[1]

# TODO: Create a TCP socket and use it in a 'with' statement for automatic cleanup
with # Your code here as server:
    
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    # TODO: Bind the server socket to the server address
    # Your code here
    
    # TODO: Start listening for connections (accept 1 connection at a time)
    # Your code here
    
    server.settimeout(1.0)
    
    while True:
        try:
            # TODO: Accept a client connection
            client, client_addr = # Your code here
            
            print("Connected:", client_addr)
            
            # TODO: Receive data from client (receive exactly unpacker.size bytes)
            data = # Your code here
            
            print("Received:", data)
            
            unp_data = unpacker.unpack(data)
            print("Unpack:", unp_data)
            
            x = eval(str(unp_data[0]) + unp_data[2].decode() + str(unp_data[1]))
            
            # TODO: Send the result back to the client (remember to encode the string)
            # Your code here
            
        except timeout:
            pass