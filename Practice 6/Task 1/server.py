import sys
import socket
import struct

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

# TODO 1: Create a UDP socket (SOCK_DGRAM).
sock = # ...

# TODO 2: Bind the socket to the server's address and port.
# ...

ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: int(x / y),
}
packer = struct.Struct("i i c")

print("UDP server is listening...")

while True:
    try:
        # TODO 3: Receive data from a client.
        # recvfrom() returns the data and the client's address.
        # Use packer.size as the buffer size.
        data, client_addr = # ...

        parsed_msg = packer.unpack(data)
        result = ops[parsed_msg[2].decode()](parsed_msg[0], parsed_msg[1])
        msg = packer.pack(result, 0, b"R")
        
        # TODO 4: Send the resulting message back to the client's address.
        # ...

    except KeyboardInterrupt:
        print("\nServer shutting down.")
        break

# TODO 5: Close the socket.
# ...