from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout, error
import sys

server_addr = ("", int(sys.argv[1]))

# TODO: Create a TCP socket and use it in a 'with' statement (hint: socket(AF_INET, SOCK_STREAM))
with # Your code here as server:
    
    # TODO: Bind the server to the server address (hint: use bind())
    # Your code here
    
    # TODO: Start listening with backlog of 0 (hint: use listen(0))
    # Your code here
    
    while True:
        try:
            # TODO: Accept a client connection (hint: use accept())
            client, client_addr = # Your code here
            
            print("Connected:", client_addr)
            
            # TODO: Receive data from client and decode it (hint: use recv(256).decode())
            data = # Your code here
            
            print("Received:", data)
            
            # TODO: Send "Hello Client!" back to client (hint: use send() and encode())
            # Your code here
            
            # TODO: Close the client socket (hint: use close())
            # Your code here
            
        except error:
            pass