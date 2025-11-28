# lottery_server_udp.py
import sys
import socket
import random

# --- Solves Task I.b (UDP) + Task II.a (bytes with ':' separator) ---


def generate_drawn_numbers():
    """Generate 5 unique random numbers between 1 and 20"""
    return random.sample(range(1, 21), 5)


def calculate_winnings(drawn_numbers, picked_numbers, bet_amount):
    """Calculate winnings based on matching numbers"""
    hits = len(set(drawn_numbers) & set(picked_numbers))
    return hits * bet_amount


def run_lottery_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        print(f"Lottery UDP server listening on {ip}:{port}")

        try:
            while True:
                data, client_addr = sock.recvfrom(1024)

                # Parse message: "num1:num2:num3:num4:num5:bet_amount"
                try:
                    parts = data.decode().split(":")
                    picked_numbers = [int(parts[i]) for i in range(5)]
                    bet_amount = int(parts[5])

                    print(
                        f"Client {client_addr} picked {picked_numbers}, bet ${bet_amount}"
                    )

                    # Generate drawn numbers
                    drawn_numbers = generate_drawn_numbers()

                    # Calculate winnings
                    winnings = calculate_winnings(
                        drawn_numbers, picked_numbers, bet_amount
                    )

                    print(f"Drawn numbers: {drawn_numbers}, Winnings: ${winnings}")

                    # Send response: "drawn1:drawn2:drawn3:drawn4:drawn5:winnings"
                    response = ":".join(map(str, drawn_numbers)) + f":{winnings}"
                    sock.sendto(response.encode(), client_addr)
                    print(f"Sent response to {client_addr}")

                except (ValueError, IndexError) as e:
                    print(f"Invalid message format from {client_addr}: {e}")
                    sock.sendto(b"ERROR:Invalid format", client_addr)

        except KeyboardInterrupt:
            print("\nLottery UDP server shutting down.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 lottery_server_udp.py <listen_ip> <listen_port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])

    run_lottery_server(listen_ip, listen_port)
