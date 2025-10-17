import sys
import socket
import struct
import select

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

# TODO 1: Create a TCP socket (SOCK_STREAM).
sock = # ...

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# TODO 2: Bind the socket to the address this server should listen on.
# ...

# TODO 3: Set the socket to listen for incoming connections.
# ...

print(f"TCP Calculator Server listening on {server_addr}:{server_port}")

ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,
}
packer = struct.Struct("i i 1s")
inputs = [sock]
timeout = 1.0

while True:
    try:
        readables, _, _ = select.select(inputs, [], [], timeout)

        for s in readables:
            # If the readable socket is the main one, it's a new connection.
            if s is sock:
                # TODO 4: Accept the new connection.
                connection, client_info = # ...
                
                print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                inputs.append(connection)
            # Otherwise, it's an existing client sending data.
            else:
                # TODO 5: Receive the calculation data from the client 's'.
                # Use packer.size for the buffer size.
                msg = # ...
                
                if not msg:
                    s.close()
                    print("The client has terminated the connection")
                    inputs.remove(s)
                    continue

                operand_a, operand_b, operator = packer.unpack(msg)
                operator = operator.decode()
                print(f"The client's message: {operand_a} {operator} {operand_b}")
                
                result = ops[operator](operand_a, operand_b)
                msg = packer.pack(result, 0, b"R")
                
                # TODO 6: Send the result back to the client 's'.
                # ...
                
                print(f"Sent response: {result}")

    except KeyboardInterrupt:
        for s in inputs:
            s.close()
        print("\nServer closing")
        break