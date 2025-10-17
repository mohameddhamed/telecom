import socket

# TODO 1: Use a 'with' statement to create a UDP socket (AF_INET, SOCK_DGRAM) and assign it to 'sock'.
# The code below this comment should be indented to be inside the 'with' block.

	# This option allows the server to be restarted immediately after closing.
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	server_address = ('localhost', 10001)
	
	# TODO 2: Bind the socket to the 'server_address'.
	# This tells the operating system that this script will handle incoming packets
	# for this specific address and port.
	

	# Setting a timeout is not required, but it allows the program
	# to gracefully handle being shut down with Ctrl+C.
	sock.settimeout(1.0)

	print("UDP server is up and listening...")

	while True:
		try:
			# TODO 3: Receive data from a client (e.g., buffer size 200).
			# recvfrom() returns both the data and the address of the client that sent it.
			# Assign these to variables named 'data' and 'client'.
			

			print ('Received: ', data.decode())

			# TODO 4: Send the string "Hello client!" back to the 'client' address.
			# Remember to .encode() the string to bytes.
			

		except socket.timeout:
			# This happens if no data is received for 1.0 seconds.
			pass
		except socket.error as msg:
			print(msg)