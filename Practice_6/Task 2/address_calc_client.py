import sys
import socket
import random
import struct
import time

ASK_FOR_ADDRESS_MSG = "Hello server".encode()
BUFFER_SIZE = 200

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

# --- Phase 1: Service Discovery via UDP ---

# TODO 1: Create a UDP socket (SOCK_DGRAM) for discovery.
udp_sock = # ...

# TODO 2: Send the discovery message to the UDP server.
print(f"Asking UDP server {server_addr}:{server_port} for the calculator's address...")
# ...

# TODO 3: Receive the TCP server's address from the UDP server.
address, _ = # ...
udp_sock.close() # We are done with the UDP socket.

# Parse the received address
calc_ip, calc_port = address.decode().split(":")
calc_port = int(calc_port)
print(f"Received calculator address: {calc_ip}:{calc_port}")

# --- Phase 2: Communication with Calculator via TCP ---

# TODO 4: Create a TCP socket (SOCK_STREAM) for calculations.
sock = # ...

# TODO 5: Connect the TCP socket to the newly discovered calculator address.
# ...

ops = ["+", "-", "*", "/"]
packer = struct.Struct("i i 1s")

for nrnd in range(5):
    operand_a = random.randint(1, 100)
    operand_b = random.randint(1, 100)
    operator = random.choice(ops)

    msg = packer.pack(operand_a, operand_b, operator.encode())
    print(f"Message: {operand_a} {operator} {operand_b}")
    
    # TODO 6: Send the calculation message over the TCP connection.
    # ...

    # TODO 7: Receive the result from the TCP server.
    msg = # ...
    
    parsed_msg = packer.unpack(msg)
    print(f"Received result: {parsed_msg[0]}")
    time.sleep(2)

# TODO 8: Close the TCP socket.
# ...