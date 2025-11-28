# instructor_server_task1.py
import sys
import socket

# --- Solves Task I ---
# - A simple TCP server.
# - Handles one client at a time in a blocking loop.
# - The "sufficient number" of students is hardcoded to 1 for this simple example.


def run_instructor_server(ip, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(1)

    print(f"Instructor server (Task 1 version) listening on {ip}:{port}")
    print("This server handles one student at a time.")

    try:
        while True:
            # Wait for and accept a single connection
            connection, client_addr = server_sock.accept()
            with connection:
                print(f"New student connected from {client_addr}")

                # Wait for the task request
                data = connection.recv(1024)
                if data == b"I would like a task":
                    print("Student requested a task.")

                    # For Task 1, we can simplify and assume 1 student is "sufficient".
                    # We first reply "Not yet" to show the logic.
                    connection.sendall(b"Not yet")
                    print("Sent: 'Not yet'")

                    # Then we immediately decide it's time for the task.
                    print("Decided to create a task...")
                    connection.sendall(b"Here is the task!")
                    print("Sent: 'Here is the task!'")

                    # Wait for the "Thank you"
                    thanks = connection.recv(1024)
                    if thanks == b"Thank you":
                        print("Student said thank you.")
                        connection.sendall(b"You're welcome")
                        print("Sent: 'You're welcome'")

                print(f"Finished with student {client_addr}. Waiting for next student.")

    except KeyboardInterrupt:
        print("\nInstructor server shutting down.")
    finally:
        server_sock.close()


if __name__ == "__main__":
    run_instructor_server("localhost", 10001)
