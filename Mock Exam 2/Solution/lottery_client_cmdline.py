# lottery_client_cmdline.py
import sys
import socket

# --- Solves Task I.a (TCP) + Task II.a (bytes with ':') + Task IV.d (command line args) ---


def run_lottery_client(ip, port, picked_numbers, bet_amount):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print(f"Connecting to lottery server at {ip}:{port}...")
            sock.connect((ip, port))

            print(f"Picked numbers: {picked_numbers}")
            print(f"Bet amount: ${bet_amount}")

            # Send message: "num1:num2:num3:num4:num5:bet_amount"
            message = ":".join(map(str, picked_numbers)) + f":{bet_amount}"
            sock.sendall(message.encode())
            print(f"Sent: '{message}'")

            # Receive response
            response = sock.recv(1024)
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

        except ConnectionRefusedError:
            print("Connection refused. Is the lottery server running?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Closing connection.")


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print(
            "Usage: python3 lottery_client_cmdline.py <server_ip> <server_port> <num1> <num2> <num3> <num4> <num5> <bet>"
        )
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    picked_numbers = [int(sys.argv[i]) for i in range(3, 8)]
    bet_amount = int(sys.argv[8])

    run_lottery_client(server_ip, server_port, picked_numbers, bet_amount)
