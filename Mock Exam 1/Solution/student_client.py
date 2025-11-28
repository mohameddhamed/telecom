import sys
import socket
import time


def run_student_client(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print(f"Connecting to instructor at {ip}:{port}...")
            sock.connect((ip, port))

            # Send initial request
            sock.sendall(b"I would like a task")
            print("Sent: 'I would like a task'")

            # Wait for the task, handling "Not yet"
            while True:
                response = sock.recv(1024)
                if not response:
                    print("Instructor closed the connection unexpectedly.")
                    return

                if response == b"Not yet":
                    print("Received: 'Not yet'. Waiting...")
                    time.sleep(2)  # Wait a bit before checking again
                else:
                    print(f"Received task: '{response.decode()}'")
                    break

            # Say thank you
            sock.sendall(b"Thank you")
            print("Sent: 'Thank you'")

            # Get the final response
            final_response = sock.recv(1024)
            print(f"Received: '{final_response.decode()}'")

        except ConnectionRefusedError:
            print("Connection refused. Is the instructor server running?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Closing connection.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 student_client.py <instructor_ip> <instructor_port>")
        sys.exit(1)

    instructor_ip = sys.argv[1]
    instructor_port = int(sys.argv[2])

    run_student_client(instructor_ip, instructor_port)
