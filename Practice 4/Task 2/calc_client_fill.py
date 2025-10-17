# calc_client_fill.py
#
# Student exercise: Fill in the TODO sections to complete the TCP calculator client.
# This client will send 5 random arithmetic problems to the server and print the results.

import sys
import socket
import random
import struct
import time

# --- Boilerplate: Parsing command line arguments ---
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <server_addr> <server_port>")
    sys.exit(1)

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

# --- Student exercise starts here ---

# TODO 1: Create a new socket object for IPv4 and TCP communication.
# Use the socket.AF_INET address family for IPv4 and socket.SOCK_STREAM for TCP.
sock = None  # Replace None with the correct socket creation call

# TODO 2: Connect the socket to the server's address and port.
# The server address and port are stored in the server_addr and server_port variables.


# List of possible operations
ops = ["+", "-", "*", "/"]

# TODO 3: Create a Struct object for packing the data.
# The message format is: one integer, another integer, and a 1-character string.
# The format string for this is "i i 1s".
packer = None  # Replace None with the correct Struct object

# Loop to send 5 random calculations
for nrnd in range(5):
    # Generate random operands and an operator
    operand_a = random.randint(1, 100)
    operand_b = random.randint(1, 100)
    operator = random.choice(ops)

    print(f"Message: {operand_a} {operator} {operand_b}")

    # TODO 4: Pack the two operands and the operator into a binary message.
    # Don't forget to encode the operator string into bytes before packing.
    msg = None  # Replace None with the call to packer.pack()

    # TODO 5: Send the packed message to the server.
    # The sendall() method is recommended as it handles sending all data.

    # TODO 6: Receive the response from the server.
    # The response will have the same size as the messages we send, so you can use packer.size
    # to specify how many bytes to receive.
    msg = None  # Replace None with the call to sock.recv()

    # TODO 7: Unpack the received message to get the result.
    # The result is the first element in the unpacked tuple.
    parsed_msg = None  # Replace None with the call to packer.unpack()
    result = parsed_msg[0]

    print(f"Received result: {result}")
    time.sleep(2)

# TODO 8: Close the socket connection.
# It's important to clean up resources when you're done.


print("Client finished.")
