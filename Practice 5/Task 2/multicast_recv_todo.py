import socket
import struct
import sys
import time

multicast_group = '224.1.1.1'
server_address = ('', 10000) # Listen on all available interfaces

# TODO 1: Create a UDP socket (AF_INET, SOCK_DGRAM).
sock = # ...

# TODO 2: Bind the socket to the 'server_address'.
# This allows the socket to receive messages on port 10000.
sock.bind(# ...)
sock.settimeout(1.0)

# --- Tell the OS to join the multicast group ---
# First, convert the multicast group IP string to a 32-bit packed binary format.
group = socket.inet_aton(multicast_group)

# TODO 3: Create the membership request structure.
# This structure tells the OS which multicast group we want to join
# and on which network interface. socket.INADDR_ANY means "join on all available interfaces".
# Use struct.pack() with the format '4sL' (4-byte string, unsigned Long).
mreq = struct.pack(# ..., group, socket.INADDR_ANY)

# TODO 4: Set the IP_ADD_MEMBERSHIP socket option.
# This is the final step to subscribe this socket to the multicast group.
# Use sock.setsockopt() with the IPPROTO_IP level.
sock.setsockopt(# ..., # ..., mreq)

# Receive/respond loop
while True:
	try:
		print ( '\nwaiting to receive message')
		
		# TODO 5: Receive data from the socket.
		# Use a large buffer size (e.g., 1024) to be safe.
		data, address = sock.recvfrom(# ...)

		print ('received %s bytes from %s : %s' % (len(data), address, data.decode()))
		time.sleep(1.0)
		
		print ('sending acknowledgement to', address)
		# TODO 6: Send an 'ack' message back to the sender's 'address'.
		# This is a unicast response, not a multicast.
		sock.sendto(# ..., address)
	except (socket.timeout, KeyboardInterrupt):
		# Pass on timeout, or break the loop on Ctrl+C (KeyboardInterrupt)
		pass