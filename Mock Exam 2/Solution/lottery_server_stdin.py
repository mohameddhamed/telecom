# lottery_server_struct.py
import sys
import socket
import select
import random
import struct

# --- Solves Task I.a (TCP) + Task II.b (struct format) + Task III (select) ---


def generate_drawn_numbers():
    """Generate 5 unique random numbers between 1 and 20"""
    return random.sample(range(1, 21), 5)


def calculate_winnings(drawn_numbers, picked_numbers, bet_amount):
    """Calculate winnings based on matching numbers"""
    hits = len(set(drawn_numbers) & set(picked_numbers))
    return hits * bet_amount


def run_lottery_server(ip, port):
    # Format: 5 integers (picked numbers) + 1 integer (bet amount)
    request_format = struct.Struct("i i i i i i")
    # Format: 5 integers (drawn numbers) + 1 integer (winnings)
    response_format = struct.Struct("i i i i i i")

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(5)

    inputs = [server_sock]

    print(f"Lottery TCP server (struct format) listening on {ip}:{port}")

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
                        try:
                            # Unpack the request
                            unpacked = request_format.unpack(
                                data[: request_format.size]
                            )
                            picked_numbers = list(unpacked[:5])
                            bet_amount = unpacked[5]

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

                            # Pack and send response
                            response_data = drawn_numbers + [winnings]
                            response = response_format.pack(*response_data)
                            s.sendall(response)

                        except struct.error as e:
                            print(f"Invalid message format from {s.getpeername()}: {e}")

    except KeyboardInterrupt:
        print("\nLottery server shutting down.")
    finally:
        for s in inputs:
            s.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 lottery_server_struct.py <listen_ip> <listen_port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])

    run_lottery_server(listen_ip, listen_port)
