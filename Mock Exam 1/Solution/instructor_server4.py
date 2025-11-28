# instructor_server_task4.py
import sys
import socket
import select
import random

# --- Solves Tasks I, II, III, & IV (Complete Solution) ---
# - Builds on the concurrent server from Task 3.
# - Adds the UDP client functionality to contact the exam archive server.
# - The final, complete solution as provided previously.


def run_instructor_server(ip, port, sufficient_students, archive_ip, archive_port):
    # TCP listening socket for students
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(5)

    # UDP socket to contact the archive server
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    archive_address = (archive_ip, archive_port)

    inputs = [server_sock]
    waiting_students = []

    print(f"Instructor server (Task 4 version) listening on {ip}:{port}")
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

                        print(
                            f"Total students waiting: {len(waiting_students)}/{sufficient_students}"
                        )

                        if len(waiting_students) >= sufficient_students:
                            print(
                                "Sufficient number reached. Contacting archive server..."
                            )

                            # Task IV: Contact the Previous Years' Exam Server via UDP
                            udp_sock.sendto(b"Search", archive_address)
                            task_response, _ = udp_sock.recvfrom(1024)

                            print(
                                f"Received task '{task_response.decode()}' from archive."
                            )

                            final_message = (
                                b"Here is the task! Your task is: " + task_response
                            )

                            print("Broadcasting task to all waiting students...")
                            for student_sock in waiting_students:
                                student_sock.sendall(final_message)

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
        udp_sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python3 instructor_server_task4.py <listen_ip> <listen_port> <num_students> <archive_ip> <archive_port>"
        )
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    num_students = int(sys.argv[3])
    archive_ip = sys.argv[4]
    archive_port = int(sys.argv[5])

    if not (1 <= num_students <= 5):
        print("Error: Number of students must be between 1 and 5.")
        sys.exit(1)

    run_instructor_server(
        listen_ip, listen_port, num_students, archive_ip, archive_port
    )
