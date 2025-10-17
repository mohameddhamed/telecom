# server_solution.py

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

# --- Solution starts here ---

# 1: Create the main server socket for IPv4 and TCP.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2: Set the SO_REUSEADDR option on the socket.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3: Bind the socket to the server_address.
server_socket.bind(server_address)

# 4: Start listening for incoming connections.
server_socket.listen(5)

# List of sockets to monitor with select(). Initially, it's just the server socket.
sockets_to_monitor = [server_socket]

print(f"Server listening on {host}:{port}")

try:
    while True:
        # 5: Use select.select() to get lists of sockets that are ready.
        readable_sockets, _, _ = select.select(sockets_to_monitor, [], [])

        # Iterate over the sockets that have incoming data
        for sock in readable_sockets:
            # If the readable socket is the main server socket, it means a new client is trying to connect.
            if sock is server_socket:
                # 6: Accept the new connection.
                client_socket, client_address = server_socket.accept()

                print(
                    f"Accepted new connection from {client_address[0]}:{client_address[1]}"
                )

                # 7: Add the new client_socket to our list of sockets to monitor.
                sockets_to_monitor.append(client_socket)

            # Otherwise, an existing client has sent us data.
            else:
                # 8: Receive data from the client socket.
                data = sock.recv(1024)

                if data:
                    # The client sent some data.
                    print(
                        f"Received message from {sock.getpeername()}: {data.decode()}"
                    )

                    # 9: Send the required b"OK" response back to the client.
                    sock.sendall(b"OK")
                else:
                    # If recv() returns an empty bytestring, the client has disconnected.
                    print(f"Client {sock.getpeername()} disconnected.")

                    # 10: Remove the socket from our list of sockets to monitor.
                    sockets_to_monitor.remove(sock)

                    # 11: Close the disconnected client's socket.
                    sock.close()

except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    # 12: Clean up by closing all sockets that are still open.
    for sock in sockets_to_monitor:
        sock.close()
