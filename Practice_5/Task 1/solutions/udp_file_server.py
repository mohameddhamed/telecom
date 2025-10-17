# udp_file_server_solution.py
import socket

SERVER_ADDRESS = ("localhost", 10001)
OUTPUT_FILENAME = "received_image.png"
BUFFER_SIZE = 4096  # A large buffer to ensure we receive the whole chunk

# TODO 1: Create a UDP socket and bind it to the SERVER_ADDRESS.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(SERVER_ADDRESS)
    print(f"Server is listening on {SERVER_ADDRESS}")

    # TODO 2: Open a new file for writing in binary mode ('wb').
    with open(OUTPUT_FILENAME, "wb") as f:
        print(f"Ready to receive data. Output will be saved to '{OUTPUT_FILENAME}'")

        while True:
            try:
                # TODO 3: Receive a chunk of data and the client's address.
                data, client_address = sock.recvfrom(BUFFER_SIZE)

                # TODO 4: Check if the received data is empty.
                if not data:
                    print("End-of-file signal received from client.")
                    # If it's the end, break out of the loop.
                    break

                # TODO 5: If data was received, write it to the output file.
                f.write(data)

                print(
                    f"Received {len(data)} bytes from {client_address}. Wrote to file."
                )

                # TODO 6: Send an acknowledgment (b"OK") back to the client.
                sock.sendto(b"OK", client_address)

            except Exception as e:
                print(f"An error occurred: {e}")
                break

    print(f"File '{OUTPUT_FILENAME}' has been saved successfully.")
