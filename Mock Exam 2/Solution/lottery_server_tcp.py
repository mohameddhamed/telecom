# lottery_server_tcp.py
import sys
import socket
import select
import random

# --- Solves Task I.a (TCP) + Task II.a (bytes with ':' separator) + Task III (select) ---


def generate_drawn_numbers():
    """Generate 5 unique random numbers between 1 and 20"""
    return random.sample(range(1, 21), 5)


def calculate_winnings(drawn_numbers, picked_numbers, bet_amount):
    """Calculate winnings based on matching numbers"""
    hits = len(set(drawn_numbers) & set(picked_numbers))
    return hits * bet_amount


def run_lottery_server(ip, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(5)

    inputs = [server_sock]

    print(f"Lottery TCP server listening on {ip}:{port}")

    try:
        while True:
            readables, _, _ = select.select(inputs, [], [])

            for s in readables:
                if s is server_sock:
                    connection, client_addr = s.accept()
                    print(f"New client connected from {client_addr}")
                    inputs.append(connection)
                else:
                    data = s.recv(1024)
                    if not data:
                        print(f"Client {s.getpeername()} disconnected.")
                        inputs.remove(s)
                        s.close()
                    else:
                        # Parse message: "num1:num2:num3:num4:num5:bet_amount"
                        try:
                            parts = data.decode().split(":")
                            picked_numbers = [int(parts[i]) for i in range(5)]
                            bet_amount = int(parts[5])

                            print(
                                f"Client {s.getpeername()} picked {picked_numbers}, bet ${bet_amount}"
                            )

                            # Generate drawn numbers
                            drawn_numbers = generate_drawn_numbers()

                            # Calculate winnings
                            winnings = calculate_winnings(
                                drawn_numbers, picked_numbers, bet_amount
                            )

                            print(
                                f"Drawn numbers: {drawn_numbers}, Winnings: ${winnings}"
                            )

                            # Send response: "drawn1:drawn2:drawn3:drawn4:drawn5:winnings"
                            response = (
                                ":".join(map(str, drawn_numbers)) + f":{winnings}"
                            )
                            s.sendall(response.encode())

                        except (ValueError, IndexError) as e:
                            print(f"Invalid message format from {s.getpeername()}: {e}")
                            s.sendall(b"ERROR:Invalid format")

    except KeyboardInterrupt:
        print("\nLottery server shutting down.")
    finally:
        for s in inputs:
            s.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 lottery_server_tcp.py <listen_ip> <listen_port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])

    run_lottery_server(listen_ip, listen_port)
