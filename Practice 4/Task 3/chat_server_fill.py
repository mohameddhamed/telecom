# chat_server_fill.py
#
# Student exercise: Fill in the TODO sections to complete the chat server.
# This server uses select() to handle multiple clients simultaneously.

import socket
from select import select
import queue
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, error

server_address = ("", 10000)

# --- Student exercise starts here ---

# TODO 1: Create the main server socket for IPv4 and TCP.
server = None  # Replace None with the correct socket creation call

# We'll be using select, so the socket can be non-blocking, but the original
# code uses a timeout. We will keep the timeout for simplicity.
server.settimeout(1.0)

# TODO 2: Set the SO_REUSEADDR socket option.
# This allows the server to be restarted quickly.
# Use SOL_SOCKET for the level, SO_REUSEADDR for the option, and 1 for the value.


# TODO 3: Bind the server socket to the server_address.


# TODO 4: Put the socket into listening mode to accept incoming connections.
# A backlog of 5 is a standard value.


# TODO 5: Initialize the list of sockets that `select` will monitor.
# It should initially contain just the main server socket.
inputs = []  # Add the server socket to this list

# Message queue for decoupling receiving from sending
msg_q = queue.Queue()
# Dictionary to map socket objects to usernames
username = {}

print("Chat server started on port 10000.")

while inputs:
    timeout = 1
    # TODO 6: Call select.select() to get lists of readable, writable, and exceptional sockets.
    # We want to check for readability on all sockets in `inputs`.
    # We want to check for writability on all sockets in `inputs` as well, so we can send messages.
    # We are also interested in exceptional conditions.
    readable, writeable, exceptable = ([], [], [])  # Replace with the call to select()

    # If select returns no active sockets, continue the loop
    if not (readable or writeable or exceptable):
        continue

    # --- Handle readable sockets ---
    for s in readable:
        try:
            # If the readable socket is the main server socket, it's a new connection.
            if s is server:
                # TODO 7: Accept the new connection.
                # This returns a new socket for the client and the client's address.
                client, client_addr = (
                    None,
                    None,
                )  # Replace with the call to s.accept()

                client.setblocking(1)  # Set to blocking for the initial username recv

                # TODO 8: Receive the username from the new client.
                # A small buffer (e.g., 20 bytes) is enough. Remember to decode and strip it.
                name = ""  # Replace with the call to client.recv()

                print(f"Client connected: {name} from {client_addr}")
                username[client] = name

                # TODO 9: Add the new client socket to the `inputs` list to be monitored.

                msg_q.put((name, "has logged in"))

            # Otherwise, it's an existing client that sent data.
            else:
                # TODO 10: Receive data from the client socket `s`.
                # Use a buffer of 200 bytes.
                data = None  # Replace with the call to s.recv()

                if data:
                    # Add the received message to the queue to be broadcast.
                    msg_q.put((username[s], data.decode().strip()))
                else:
                    # An empty message means the client disconnected.
                    print(f"Client disconnected: {username[s]}")
                    msg_q.put((username[s], "has logged out"))

                    # TODO 11: Remove the socket from the `inputs` list.

                    # Also remove it from writeable list if it's there
                    if s in writeable:
                        writeable.remove(s)

                    # TODO 12: Close the disconnected client's socket.

        except error as m:
            print("Socket Error", m)
            inputs.remove(s)
            if s in writeable:
                writeable.remove(s)
            s.close()

    # --- Distribute messages from the queue to all writable sockets ---
    while not msg_q.empty():
        try:
            next_msg = msg_q.get_nowait()
        except queue.Empty:
            break
        else:
            # Loop through clients that are ready to receive data.
            for s in writeable:
                # Don't send a user's message back to themselves.
                # We also don't send to the main server listening socket.
                if s is not server and username[s] != next_msg[0]:

                    # TODO 13: Send the formatted message to the client socket `s`.
                    # The message format is "[sender_name] message_content".
                    # Remember to encode the final string.
                    msg_to_send = f"[{next_msg[0]}] {next_msg[1]}"
                    # Add the sendall call here

                    print(f"Sent to: {username[s]}")
