# chat_client_fill.py
#
# Student exercise: Fill in the TODO sections to complete the chat client.
# This client connects to a chat server, sends the user's name, and then
# enters a loop to send and receive messages.

import socket
import sys
from input_timeout import readInput
from socket import timeout, error

# --- Boilerplate: Get username from command line and set server address ---
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <username>")
    sys.exit(1)
username = sys.argv[1]
server_address = ("localhost", 10000)


# --- Helper function for displaying the input prompt ---
def prompt(nl):
    if nl:
        print("")
    print("<" + username + ">", end=" ", flush=True)


# --- Student exercise starts here ---

# TODO 1: Create a new socket object for IPv4 and TCP communication.
client = None  # Replace None with the correct socket creation call

# TODO 2: Connect the socket to the server's address.
# The server address is a tuple (host, port).


# TODO 3: Send the username to the server.
# The server expects the username as the very first message.
# Remember to encode the string into bytes before sending.


# TODO 4: Set a non-blocking timeout on the socket.
# A timeout of 1.0 second is good. This will make client.recv() raise a
# socket.timeout exception if no data arrives within 1 second.
# This is crucial for making the main loop feel responsive.


prompt(False)

while True:
    try:
        # TODO 5: Try to receive data from the server.
        # Use a buffer size of 200 bytes. This call will block for at most
        # the timeout duration set in the previous step.
        data = None  # Replace None with the call to client.recv()

        if not data:
            print("Server down")
            break
        else:
            print("\n" + data.decode())  # Print message from another user
            sys.stdout.flush()
            prompt(False)
    except SystemExit:
        break
    except timeout:
        # This is not an error. It just means no data was received from the
        # server in the last second. We can ignore it and proceed to check for user input.
        pass
    except error as e:
        print("Socket Error", e)
        break

    try:
        # Check for user input from the keyboard (non-blocking)
        msg = readInput()
        msg = msg.strip()
        if msg != "":
            # TODO 6: Send the user's typed message to the server.
            # Don't forget to encode the string.

            prompt(True)
    except timeout:
        pass
    except error as e:
        print("Socket Error", e)
        break

# TODO 7: Close the client socket when the loop is finished.
print("Closing connection.")
