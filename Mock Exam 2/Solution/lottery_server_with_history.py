# lottery_server_with_history.py
import sys
import socket
import select
import random

# --- Solves Task V.b - lottery server that sends logs to separate history server ---


def generate_drawn_numbers():
    """Generate 5 unique random numbers between 1 and 20"""
    return random.sample(range(1, 21), 5)


def calculate_winnings(drawn_numbers, picked_numbers, bet_amount):
    """Calculate winnings based on matching numbers"""
    hits = len(set(drawn_numbers) & set(picked_numbers))
    return hits * bet_amount


def send_to_history_server(
    udp_sock, history_addr, picked_numbers, bet_amount, drawn_numbers, winnings
):
    """Send log data to history server via UDP"""
    try:
        # Format: "picked1:...:picked5:bet:drawn1:...:drawn5:winnings"
        log_message = ":".join(map(str, picked_numbers)) + f":{bet_amount}:"
        log_message += ":".join(map(str, drawn_numbers)) + f":{winnings}"

        udp_sock.sendto(log_message.encode(), history_addr)
        print(f"Sent log to history server at {history_addr}")

    except Exception as e:
        print(f"Error sending to history server: {e}")


def run_lottery_server(ip, port, history_ip, history_port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))
    server_sock.listen(5)

    # UDP socket for history server
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    history_address = (history_ip, history_port)

    inputs = [server_sock]

    print(f"Lottery TCP server listening on {ip}:{port}")
    print(f"Will log to history server at {history_ip}:{history_port}")

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

                            # Send to history server
                            send_to_history_server(
                                udp_sock,
                                history_address,
                                picked_numbers,
                                bet_amount,
                                drawn_numbers,
                                winnings,
                            )

                            # Send response to client: "drawn1:drawn2:drawn3:drawn4:drawn5:winnings"
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
        udp_sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python3 lottery_server_with_history.py <listen_ip> <listen_port> <history_ip> <history_port>"
        )
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    history_ip = sys.argv[3]
    history_port = int(sys.argv[4])

    run_lottery_server(listen_ip, listen_port, history_ip, history_port)
