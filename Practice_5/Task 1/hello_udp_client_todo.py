import socket

# TODO 1: Use a 'with' statement to create a UDP socket (AF_INET, SOCK_DGRAM) and assign it to 'sock'.
# The code below this comment should be indented to be inside the 'with' block.

	server_address = ('localhost', 10001)

	try:
		# TODO 2: Send the string "Hello server!" to the server_address.
		# Remember to .encode() the string into bytes.
		

		# TODO 3: Receive data from the socket. Use a buffer size of 200.
		# recvfrom() returns the data and the sender's address.
		# Assign the received data to a variable called 'data' and ignore the address.
		

		print ('Received: ', data.decode())

	except socket.timeout:
		pass
	except socket.error as msg:
		print(msg)