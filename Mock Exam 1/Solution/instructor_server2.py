# instructor_server_task2.py
import sys
import socket

# --- Solves Tasks I & II ---
# - Same simple, single-client server as Task 1.
# - Adds the requirement from Task II: the sufficient number of students
#   is now a command-line argument.
# - Note: Since it only handles one client, the "sufficient number" will
#   only work correctly if set to 1. This highlights the need for concurrency.


def run_instructor_server(ip, port, sufficient_students):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(1)

    print(f"Instructor server (Task 2 version) listening on {ip}:{port}")
    print(f"Sufficient number of students set to: {sufficient_students}")

    students_served = 0
    try:
        while True:
            connection, client_addr = server_sock.accept()
            with connection:
                print(f"New student connected from {client_addr}")
                data = connection.recv(1024)

                if data == b"I would like a task":
                    print("Student requested a task.")
                    students_served += 1

                    if students_served >= sufficient_students:
                        print("Sufficient number of students reached. Sending task.")
                        connection.sendall(b"Here is the task!")

                        # Reset for the next wave of students
                        students_served = 0
                    else:
                        connection.sendall(b"Not yet")

                    # This part is simplified for a single-client server
                    thanks = connection.recv(1024)
                    if thanks == b"Thank you":
                        connection.sendall(b"You're welcome")

                print(f"Finished with student {client_addr}.")

    except KeyboardInterrupt:
        print("\nInstructor server shutting down.")
    finally:
        server_sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python3 instructor_server_task2.py <listen_ip> <listen_port> <num_students>"
        )
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    num_students = int(sys.argv[3])

    run_instructor_server(listen_ip, listen_port, num_students)
