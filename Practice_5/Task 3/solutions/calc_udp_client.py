import binascii
import socket
import struct
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 10001)

packer = struct.Struct("I I 1s")

try:
    s1 = input("Enter a number:")
    muv = input("Enter an operator:")
    s2 = input("Enter another number:")
    values = (int(s1), int(s2), muv.encode())
    packed_data = packer.pack(*values)
    print("Sending:", values)
    sock.sendto(packed_data, server_address)
    data, _ = sock.recvfrom(16)
    print("Result: ", data.decode())

finally:
    print("Closing socket")
    sock.close()
