# instructor_server_task3.py
import sys
import socket
import select

# --- Solves Tasks I, II, & III ---
# - Major architectural change to handle multiple clients concurrently using select().
# - Takes the sufficient number of students as a command-line argument.
# - Maintains a list of "waiting_students" and broadcasts the task to all of them.


def run_instructor_server(ip, port, sufficient_students):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(5)

    inputs = [server_sock]
    waiting_students = []

    print(f"Instructor server (Task 3 version) listening on {ip}:{port}")
    print(f"Waiting for {sufficient_students} students...")

    try:
        while True:
            readables, _, _ = select.select(inputs, [], [])

            for s in readables:
                if s is server_sock:
                    connection, client_addr = s.accept()
                    print(f"New student connected from {client_addr}")
                    inputs.append(connection)
                else:
                    data = s.recv(1024)
                    if not data:
                        print(f"Student {s.getpeername()} disconnected.")
                        if s in waiting_students:
                            waiting_students.remove(s)
                        inputs.remove(s)
                        s.close()
                    elif data == b"I would like a task":
                        print(f"Student {s.getpeername()} requested a task.")
                        if s not in waiting_students:
                            waiting_students.append(s)

                        if len(waiting_students) >= sufficient_students:
                            print("Sufficient number reached. Broadcasting task.")
                            for student_sock in waiting_students:
                                student_sock.sendall(b"Here is the task!")
                            waiting_students.clear()
                        else:
                            s.sendall(b"Not yet")
                    elif data == b"Thank you":
                        print(f"Student {s.getpeername()} said thank you.")
                        s.sendall(b"You're welcome")
    except KeyboardInterrupt:
        print("\nInstructor server shutting down.")
    finally:
        for s in inputs:
            s.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python3 instructor_server_task3.py <listen_ip> <listen_port> <num_students>"
        )
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    num_students = int(sys.argv[3])

    if not (1 <= num_students <= 5):
        print("Error: Number of students must be between 1 and 5.")
        sys.exit(1)

    run_instructor_server(listen_ip, listen_port, num_students)
