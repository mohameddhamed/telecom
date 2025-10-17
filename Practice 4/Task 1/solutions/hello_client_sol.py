# client_solution.py

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

# --- Solution starts here ---

# 1: Create a client socket for IPv4 and TCP.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 2: Connect the socket to the server's address.
    print(f"Connecting to {host}:{port}")
    client_socket.connect(server_address)

    # Loop to send 5 messages
    for i in range(5):
        message_to_send = f"This is message number {i+1}"
        print(f"Sending: '{message_to_send}'")

        # 3: Send the message to the server.
        client_socket.sendall(message_to_send.encode())

        # 4: Receive the response from the server.
        response = client_socket.recv(1024)

        print(f"Received: {response.decode()}")
        time.sleep(1)  # Wait a second before sending the next message

except ConnectionRefusedError:
    print("Connection refused. Is the server running?")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # 5: Close the client socket.
    print("Closing connection.")
    client_socket.close()
