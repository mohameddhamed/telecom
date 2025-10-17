import sys
import socket
import random
import struct
import time

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

# TODO 1: Create a TCP socket (SOCK_STREAM).
sock = # ...

# TODO 2: Connect the socket to the server's address and port.
# ...

ops = ["+", "-", "*", "/"]
packer = struct.Struct("i i 1s")

for nrnd in range(5):
    operand_a = random.randint(1, 100)
    operand_b = random.randint(1, 100)
    operator = random.choice(ops)

    msg = packer.pack(operand_a, operand_b, operator.encode())
    print(f"Message: {operand_a} {operator} {operand_b}")
    
    # TODO 3: Send the packed message to the server.
    # Use sendall() for TCP to ensure all data is sent.
    # ...

    # TODO 4: Receive the result from the server.
    # The size of the expected message is packer.size.
    msg = # ...
    
    parsed_msg = packer.unpack(msg)
    print(f"Received result: {parsed_msg[0]}")
    time.sleep(2)

# TODO 5: Close the socket connection.
# ...