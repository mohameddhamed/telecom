from socket import socket, AF_INET, SOCK_STREAM

server_addr = ('localhost', 10000)

# TODO: Create a TCP socket using AF_INET and SOCK_STREAM
client = # Your code here

# TODO: Connect to the server using the server_addr
# Your code here

# TODO: Send "Hello Server!" to the server (remember to encode the string)
# Your code here

# TODO: Receive data from the server (up to 16 bytes)
data = # Your code here

print("Received:", data.decode())

# TODO: Close the client socket
# Your code here