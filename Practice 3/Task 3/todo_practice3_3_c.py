from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout, error
import sys

test_host, test_port_number = sys.argv[1], int(sys.argv[2])
correct = True

'''
The order of the send-recv pairs are important!
c1.connect
c2.connect
	not correct:
		c2.send
		c2.recv
		c1.send
	correct:
		c1.send
		c2.send
		c2.recv
c1.recv
'''

# TODO: Create first TCP socket (hint: use socket() with AF_INET and SOCK_STREAM)
client1 = # Your code here

client1.settimeout(0.5)

# TODO: Connect client1 to the server (hint: use connect() with tuple of host and port)
# Your code here

# TODO: Create second TCP socket
client2 = # Your code here

client2.settimeout(0.5)

# TODO: Connect client2 to the server
# Your code here

# TODO: Create third TCP socket
client3 = # Your code here

client3.settimeout(0.5)

# TODO: Connect client3 to the server
# Your code here

input('Continue')

if not correct:
    # TODO: Send 'Hello Server' to client2 (hint: use send() and encode())
    # Your code here
    
    # TODO: Receive data from client2 (hint: use recv() with buffer size 256)
    d2 = # Your code here
    d2 = d2.decode()

# TODO: Send 'Hello Server' to client1
# Your code here

if correct:
    # TODO: Send 'Hello Server' to client2
    # Your code here
    
    # TODO: Receive data from client2
    d2 = # Your code here
    d2 = d2.decode()

# TODO: Receive data from client1
d1 = # Your code here

# TODO: Send 'Hello Server' to client3
# Your code here

d1 = d1.decode()

# TODO: Receive data from client3
d3 = # Your code here
d3 = d3.decode()

# TODO: Close all three client sockets (hint: use close() method)
# Your code here - close client1
# Your code here - close client2
# Your code here - close client3

print(d1, d2, d3)