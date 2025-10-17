import socket

# TODO: Create a TCP socket using socket.AF_INET and socket.SOCK_STREAM
sock = # Your code here

server_addr = ('', 10000)  # ('localhost',10000) <- igy csak localhoston fogad

# TODO: Bind the socket to the server address
# Your code here

# TODO: Start listening for connections (accept 1 connection at a time)
# Your code here

#sock.settimeout(1.0)	# windowson

while True:
    try:
        print("Waiting...")
        
        # TODO: Accept a client connection (returns client_socket and client_addr)
        client_socket, client_addr = # Your code here
        
        print("Connected: ", client_addr)
        
        # TODO: Receive data from the client (up to 16 bytes)
        data = # Your code here
        
        print("Received:", data.decode())
        
        if data:
            # TODO: Send "Hello Client!" back to the client (remember to encode)
            # Your code here
        else:
            print("Disconnected")
            
        # TODO: Close the client socket
        # Your code here
        
    #except socket.timeout:
    #    pass
    except KeyboardInterrupt:
        sock.close()
        break