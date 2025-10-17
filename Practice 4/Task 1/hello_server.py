# server_fill.py
#
# Student exercise: Fill in the TODO sections to complete the TCP server.
# This server uses select() to handle multiple clients. When it receives any
# message from a client, it should reply with the bytestring b"OK".

import socket
import select
import sys

# --- Boilerplate: Parsing command line arguments ---
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
server_address = (host, port)

# --- Student exercise starts here ---

# TODO 1: Create the main server socket for IPv4 and TCP.
server_socket = None  # Replace None with the socket creation call

# TODO 2: Set the SO_REUSEADDR option on the socket. This is important
# to allow the server to restart quickly.
# Use socket.SOL_SOCKET, socket.SO_REUSEADDR, and 1 as arguments.


# TODO 3: Bind the socket to the server_address.


# TODO 4: Start listening for incoming connections. A backlog of 5 is fine.


# List of sockets to monitor with select(). Initially, it's just the server socket.
sockets_to_monitor = [server_socket]

print(f"Server listening on {host}:{port}")

try:
    while True:
        # TODO 5: Use select.select() to get lists of sockets that are ready.
        # We are only interested in sockets that are ready for reading.
        # The other two lists (writable, exceptional) can be ignored for this exercise.
        # The first argument to select should be our list of sockets to monitor.
        readable_sockets, _, _ = (
            [],
            [],
            [],
        )  # Replace with the call to select.select()

        # Iterate over the sockets that have incoming data
        for sock in readable_sockets:
            # If the readable socket is the main server socket, it means a new client is trying to connect.
            if sock is server_socket:
                # TODO 6: Accept the new connection.
                # This returns a new socket for the client and the client's address.
                client_socket, client_address = (
                    None,
                    None,
                )  # Replace with the call to server_socket.accept()

                print(
                    f"Accepted new connection from {client_address[0]}:{client_address[1]}"
                )

                # TODO 7: Add the new client_socket to our list of sockets to monitor.

            # Otherwise, an existing client has sent us data.
            else:
                # TODO 8: Receive data from the client socket.
                # A buffer size of 1024 bytes is standard.
                data = None  # Replace with the call to sock.recv()

                if data:
                    # The client sent some data.
                    print(
                        f"Received message from {sock.getpeername()}: {data.decode()}"
                    )

                    # TODO 9: Send the required b"OK" response back to the client.
                    # Use sendall() to ensure the whole message is sent.

                else:
                    # If recv() returns an empty bytestring, the client has disconnected.
                    print(f"Client {sock.getpeername()} disconnected.")

                    # TODO 10: Remove the socket from our list of sockets to monitor.

                    # TODO 11: Close the disconnected client's socket.


except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    # TODO 12: Clean up by closing all sockets that are still open.
    for sock in sockets_to_monitor:
        pass  # Replace pass with the code to close the socket
