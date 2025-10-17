from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct

server_addr = ('localhost', 10000)
packer = struct.Struct('I I 1s')  # int, int, char[1]

# TODO: Create a TCP socket and use it in a 'with' statement for automatic cleanup
with # Your code here as client:
    
    # TODO: Connect to the server
    # Your code here
    
    num1 = input("Enter a number:")
    op = input("Enter an operator:")
    num2 = input("Enter another number:")
    
    values = (int(num1), int(num2), op.encode())
    packed_data = packer.pack(*values)
    # packed_data = packer.pack(int(num1), int(num2), op.encode())
    
    # TODO: Send all the packed data to the server
    # Your code here
    
    # TODO: Receive the result from the server (up to 16 bytes) and decode it
    data = # Your code here
    
    print("Result:", data)