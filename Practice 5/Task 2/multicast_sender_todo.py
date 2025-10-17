import socket
import struct
import sys

message = 'very important data'
multicast_group = ('224.1.1.1', 10000)

# TODO 1: Create a UDP datagram socket (AF_INET, SOCK_DGRAM).
sock = # ...

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(1.0)

# TODO 2: Set the Time-To-Live (TTL) for the messages.
# The TTL value is an integer, but it must be packed as a single byte for the socket option.
# Use struct.pack('b', 1) to pack the value 1 into a byte.
ttl = # ...

# TODO 3: Set the IP_MULTICAST_TTL socket option.
# This tells the network how many "hops" the packet can make. A TTL of 1 keeps it on the local network.
# Use sock.setsockopt() with the IPPROTO_IP level.
sock.setsockopt(# ..., # ..., ttl)

try:
    # Send data to the multicast group
    print ( 'sending "%s"' % message)

    # TODO 4: Send the 'message' to the 'multicast_group'.
    # Remember to encode the message string into bytes.
    sent = sock.sendto(# ..., # ...)

    # Look for responses from all recipients
    while True:
        print ('waiting to receive')
        try:
            # TODO 5: Receive a response from a client.
            # Use a small buffer size (e.g., 16 bytes) since we only expect 'ack'.
            data, server = sock.recvfrom(# ...)
        except socket.timeout:
            print ('timed out, no more responses')
            # The 'break' will exit the while loop if we don't get a response.
            break
        else:
            print ('received "%s" from %s' % (data.decode(), server))
            # The 'break' exits after the first response is received.
            break

finally:
    print ('closing socket')
    # TODO 6: Close the socket.
    sock.close()