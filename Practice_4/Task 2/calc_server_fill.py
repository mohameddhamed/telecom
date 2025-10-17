# calc_server_fill.py
#
# Student exercise: Fill in the TODO sections to complete the TCP calculator server.
# This server uses select() to handle multiple clients non-blockingly.

import sys
import socket
import struct
import select

# --- Boilerplate: Parsing command line arguments ---
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <server_addr> <server_port>")
    sys.exit(1)

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

# --- Student exercise starts here ---

# TODO 1: Create a new socket object for IPv4 and TCP.
sock = None  # Replace None with the correct socket creation call

# TODO 2: Set a socket option to allow the kernel to reuse the address.
# This is useful for quickly restarting the server.
# Use socket.SOL_SOCKET for the level, socket.SO_REUSEADDR for the option, and 1 for the value.


# TODO 3: Bind the socket to the server address and port.
# This associates the socket with a specific network interface and port number.


# TODO 4: Put the socket into listening mode to wait for incoming connections.
# The argument is the "backlog", the number of unaccepted connections the system
# will allow before refusing new ones. 5 is a common value.


# Dictionary of operations
ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,  # Integer division
}

# TODO 5: Create a Struct object for packing/unpacking data.
# The format must match the client: one integer, another integer, and a 1-character string.
packer = None  # Replace None with the correct Struct object

# List of sockets to monitor for incoming data. Start with the listening socket.
inputs = [sock]
timeout = 1.0

print(f"Server started on {server_addr}:{server_port}. Waiting for connections...")

while True:
    try:
        # TODO 6: Use select.select to wait for sockets to become readable.
        # It takes three lists of sockets to watch (readable, writable, exceptional) and a timeout.
        # We are only interested in the readable list here.
        readables, _, _ = (None, None, None)  # Replace with the call to select.select()

        # Loop through the sockets that are ready to be read
        for s in readables:
            # If the readable socket is the main server socket, it means there's a new connection.
            if s is sock:
                # TODO 7: Accept the new connection.
                # This returns a new socket object for the connection and the client's address.
                connection, client_info = (
                    None,
                    None,
                )  # Replace with the call to sock.accept()

                print(f"Someone has connected: {client_info[0]}:{client_info[1]}")

                # TODO 8: Add the new connection's socket to the list of inputs to monitor.

            # Otherwise, it's an existing client connection with data to read.
            else:
                # TODO 9: Receive data from the client socket `s`.
                # The message size is determined by the packer's size.
                msg = None  # Replace with the call to s.recv()

                # If recv returns an empty byte string, the client has closed the connection.
                if not msg:
                    print("The client has terminated the connection")

                    # TODO 10: Close the client's socket.

                    # TODO 11: Remove the closed socket from the list of inputs.

                    continue

                # If we received data, unpack it and perform the calculation.
                operand_a, operand_b, operator = packer.unpack(msg)
                operator = operator.decode()
                print(f"The client's message: {operand_a} {operator} {operand_b}")

                result = ops[operator](operand_a, operand_b)

                # TODO 12: Pack the result into a response message.
                # We can send back dummy values for the other two fields (e.g., 0 and b'R').
                response_msg = None  # Replace with the call to packer.pack()

                # TODO 13: Send the packed response back to the client.

                print(f"Sent response: {result}")

    except KeyboardInterrupt:
        print("\nServer closing")
        # TODO 14: Clean up by closing all sockets in the inputs list.
        for s in inputs:
            pass  # Replace pass with the code to close socket 's'
        break
