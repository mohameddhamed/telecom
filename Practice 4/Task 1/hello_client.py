# client_fill.py
#
# Student exercise: Fill in the TODO sections to complete the TCP client.
# This client will connect to the server and send five messages, printing the
# server's "OK" response after each one.

import socket
import sys
import time

# --- Boilerplate: Parsing command line arguments ---
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
server_address = (host, port)

# --- Student exercise starts here ---

# TODO 1: Create a client socket for IPv4 and TCP.
client_socket = None  # Replace None with the socket creation call

try:
    # TODO 2: Connect the socket to the server's address.
    print(f"Connecting to {host}:{port}")

    # Loop to send 5 messages
    for i in range(5):
        message_to_send = f"This is message number {i+1}"
        print(f"Sending: '{message_to_send}'")

        # TODO 3: Send the message to the server.
        # Remember to encode the string into bytes before sending.

        # TODO 4: Receive the response from the server.
        # A buffer size of 1024 is sufficient.
        response = None  # Replace with the call to client_socket.recv()

        print(f"Received: {response.decode()}")
        time.sleep(1)  # Wait a second before sending the next message

except ConnectionRefusedError:
    print("Connection refused. Is the server running?")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # TODO 5: Close the client socket.
    # This should be done regardless of whether an error occurred.
    print("Closing connection.")
