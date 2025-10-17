import sys
import socket

BUFFER_SIZE = 200

server_addr = sys.argv[1]
server_port = int(sys.argv[2])
CALC_ADDRESS = sys.argv[3].encode()

# TODO 1: Create a UDP socket (SOCK_DGRAM).
sock = # ...

# TODO 2: Bind the socket to the address this server should listen on.
# ...

print(f"UDP Address Server listening on {server_addr}:{server_port}")
print(f"Will provide this address to clients: {CALC_ADDRESS.decode()}")

while True:
    try:
        # TODO 3: Receive data and the client's address.
        # Use BUFFER_SIZE.
        data, client_addr = # ...

        # Check if the client sent the correct discovery message.
        if data.decode() == "Hello server":
            print(f"{client_addr[0]}:{client_addr[1]} has asked for the address")
            
            # TODO 4: Send the calculator's address back to the client.
            # ...
            
    except KeyboardInterrupt:
        print("\nAddress server shutting down.")
        break

# TODO 5: Close the socket.
# ...