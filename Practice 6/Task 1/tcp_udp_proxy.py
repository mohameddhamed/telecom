import sys
import socket
import struct
import select

proxy_addr = sys.argv[1]
proxy_port = int(sys.argv[2])
server_addr = sys.argv[3]
server_port = int(sys.argv[4])

packer = struct.Struct("i i 1s") # Define packer for message size calculation

# TODO 1: Create the main TCP socket for listening to clients.
sock = # ...

# TODO 2: Bind the TCP socket to the proxy's address and port.
# ...

# TODO 3: Set the TCP socket to listen for incoming connections.
# ...

# TODO 4: Create the UDP socket to communicate with the final server.
proxySock = # ...

inputs = [sock]
print("Proxy is running...")

while True:
    try:
        readables, _, _ = select.select(inputs, [], [])

        for s in readables:
            # If the readable socket is our main listening socket, it's a new connection.
            if s is sock:
                # TODO 5: Accept the new connection.
                # This returns a new socket for the connection and the client's info.
                connection, client_info = # ...
                
                print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                inputs.append(connection)
            # Otherwise, it's an existing client sending data.
            else:
                # TODO 6: Receive the message from the TCP client 's'.
                # Use packer.size for the buffer size.
                msg = # ...
                
                if not msg:
                    s.close()
                    print("The client has terminated the connection")
                    inputs.remove(s)
                    continue

                # TODO 7: Forward the message to the UDP server using the proxy's UDP socket.
                # ...
                
                # TODO 8: Receive the result back from the UDP server on the UDP socket.
                result, _ = # ...
                
                # TODO 9: Send the result back to the original TCP client 's'.
                # ...

    except KeyboardInterrupt:
        print("Proxy shutting down")
        proxySock.close()
        sock.close()
        break