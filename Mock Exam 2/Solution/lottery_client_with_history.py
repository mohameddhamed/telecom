# lottery_client_with_history.py
import sys
import socket
import random

# --- Solves Task V.c - client sends result to history server after getting result ---


def run_lottery_client(lottery_ip, lottery_port, history_ip, history_port):
    # Connect to lottery server via TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        try:
            print(f"Connecting to lottery server at {lottery_ip}:{lottery_port}...")
            tcp_sock.connect((lottery_ip, lottery_port))

            # Generate 5 random unique numbers between 1 and 20
            picked_numbers = random.sample(range(1, 21), 5)
            bet_amount = random.randint(10, 100)

            print(f"Picked numbers: {picked_numbers}")
            print(f"Bet amount: ${bet_amount}")

            # Send message: "num1:num2:num3:num4:num5:bet_amount"
            message = ":".join(map(str, picked_numbers)) + f":{bet_amount}"
            tcp_sock.sendall(message.encode())
            print(f"Sent: '{message}'")

            # Receive response
            response = tcp_sock.recv(1024)
            if not response:
                print("Server closed the connection unexpectedly.")
                return

            response_str = response.decode()
            print(f"Received: '{response_str}'")

            # Parse response: "drawn1:drawn2:drawn3:drawn4:drawn5:winnings"
            parts = response_str.split(":")
            drawn_numbers = [int(parts[i]) for i in range(5)]
            winnings = int(parts[5])

            print(f"\nDrawn numbers: {drawn_numbers}")
            print(f"Your winnings: ${winnings}")

            hits = len(set(drawn_numbers) & set(picked_numbers))
            print(f"You had {hits} matching numbers!")

            # Now send to history server via UDP
            print(
                f"\nSending results to history server at {history_ip}:{history_port}..."
            )
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
                # Format: "picked1:...:picked5:bet:drawn1:...:drawn5:winnings"
                history_message = ":".join(map(str, picked_numbers)) + f":{bet_amount}:"
                history_message += ":".join(map(str, drawn_numbers)) + f":{winnings}"

                udp_sock.sendto(history_message.encode(), (history_ip, history_port))
                print(f"Sent log to history server")

                # Wait for acknowledgment (optional)
                udp_sock.settimeout(2.0)
                try:
                    ack, _ = udp_sock.recvfrom(1024)
                    print(f"History server acknowledged: {ack.decode()}")
                except socket.timeout:
                    print("No acknowledgment from history server (timeout)")

        except ConnectionRefusedError:
            print("Connection refused. Is the lottery server running?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Closing connection.")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python3 lottery_client_with_history.py <lottery_ip> <lottery_port> <history_ip> <history_port>"
        )
        sys.exit(1)

    lottery_ip = sys.argv[1]
    lottery_port = int(sys.argv[2])
    history_ip = sys.argv[3]
    history_port = int(sys.argv[4])

    run_lottery_client(lottery_ip, lottery_port, history_ip, history_port)
