# udp_file_client_solution.py
import socket
import os

SERVER_ADDRESS = ("localhost", 10001)
FILENAME = "image_to_send.png"
CHUNK_SIZE = 200  # The size of each data chunk in bytes

# Check if the file exists and get its size
try:
    file_size = os.path.getsize(FILENAME)
except FileNotFoundError:
    print(f"Error: The file '{FILENAME}' was not found.")
    print("Please create this file in the same directory.")
    exit()

print(f"Preparing to send '{FILENAME}' ({file_size} bytes).")

# TODO 1: Create a UDP socket (socket.AF_INET, socket.SOCK_DGRAM).
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # Set a timeout for receiving ACKs from the server.
    sock.settimeout(2.0)

    # TODO 2: Open the image file for reading in binary mode ('rb').
    with open(FILENAME, "rb") as f:
        while True:
            # TODO 3: Read a chunk of data from the file.
            chunk = f.read(CHUNK_SIZE)

            # TODO 4: Send the chunk to the server address.
            sock.sendto(chunk, SERVER_ADDRESS)

            if not chunk:
                # This is the end of the file. An empty chunk is our signal.
                print("End-of-file signal sent.")
                break

            print(f"Sent {len(chunk)} bytes.")

            # Wait for acknowledgment (ACK) from the server
            try:
                # TODO 5: Receive the acknowledgment from the server.
                ack, _ = sock.recvfrom(16)

                if ack == b"OK":
                    print("ACK received.")
                else:
                    print("Error: Invalid ACK received. Stopping.")
                    break
            except socket.timeout:
                print("Error: ACK not received (timeout). Stopping.")
                break

    print("File transfer complete.")
