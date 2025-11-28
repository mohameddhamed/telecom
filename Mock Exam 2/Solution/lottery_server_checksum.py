# lottery_server_checksum.py
import sys
import socket
import select
import random
import hashlib

# --- Solves Task I.a (TCP) + Task II.c (MD5 checksum) + Task III (select) ---


def generate_drawn_numbers():
    """Generate 5 unique random numbers between 1 and 20"""
    return random.sample(range(1, 21), 5)


def calculate_winnings(drawn_numbers, picked_numbers, bet_amount):
    """Calculate winnings based on matching numbers"""
    hits = len(set(drawn_numbers) & set(picked_numbers))
    return hits * bet_amount


def verify_checksum(message, received_checksum):
    """Verify MD5 checksum"""
    calculated = hashlib.md5(message.encode()).hexdigest()
    return calculated == received_checksum


def create_checksum(message):
    """Create MD5 checksum"""
    return hashlib.md5(message.encode()).hexdigest()


def run_lottery_server(ip, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(5)

    inputs = [server_sock]

    print(f"Lottery TCP server (with MD5 checksum) listening on {ip}:{port}")

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
                        # Parse message: "num1:num2:num3:num4:num5:bet_amount:checksum"
                        try:
                            parts = data.decode().split(":")
                            picked_numbers = [int(parts[i]) for i in range(5)]
                            bet_amount = int(parts[5])
                            received_checksum = parts[6]

                            # Verify checksum
                            message_data = ":".join(parts[:6])
                            if not verify_checksum(message_data, received_checksum):
                                print(
                                    f"Checksum verification failed from {s.getpeername()}"
                                )
                                s.sendall(b"ERROR:Checksum mismatch")
                                continue

                            print(
                                f"Client {s.getpeername()} picked {picked_numbers}, bet ${bet_amount} (checksum OK)"
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

                            # Create response with checksum
                            response_data = (
                                ":".join(map(str, drawn_numbers)) + f":{winnings}"
                            )
                            checksum = create_checksum(response_data)
                            response = response_data + f":{checksum}"

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
        print("Usage: python3 lottery_server_checksum.py <listen_ip> <listen_port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])

    run_lottery_server(listen_ip, listen_port)
