import sys
import socket
import random


def run_archive_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        print(f"UDP Exam Archive Server is listening on {ip}:{port}")

        try:
            while True:
                data, client_addr = sock.recvfrom(1024)

                if data == b"Search":
                    print(f"Received 'Search' request from {client_addr}")
                    task_id = random.randint(1, 10)
                    response = f"task{task_id}".encode()
                    sock.sendto(response, client_addr)
                    print(f"Sent response '{response.decode()}' to {client_addr}")

        except KeyboardInterrupt:
            print("\nArchive server shutting down.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 exam_archive_server.py <listen_ip> <listen_port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])

    run_archive_server(listen_ip, listen_port)
