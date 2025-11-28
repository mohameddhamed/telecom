# lottery_client_proxy.py
import sys
import socket
import random

# --- Client for Task V.a (connects to proxy via UDP) ---


def run_lottery_client(proxy_ip, proxy_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            # Generate 5 random unique numbers between 1 and 20
            picked_numbers = random.sample(range(1, 21), 5)
            bet_amount = random.randint(10, 100)

            print(f"Picked numbers: {picked_numbers}")
            print(f"Bet amount: ${bet_amount}")

            # Send message to proxy: "num1:num2:num3:num4:num5:bet_amount"
            message = ":".join(map(str, picked_numbers)) + f":{bet_amount}"
            sock.sendto(message.encode(), (proxy_ip, proxy_port))
            print(f"Sent to proxy at {proxy_ip}:{proxy_port}: '{message}'")

            # Receive response from proxy
            response, _ = sock.recvfrom(1024)
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

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 lottery_client_proxy.py <proxy_ip> <proxy_port>")
        sys.exit(1)

    proxy_ip = sys.argv[1]
    proxy_port = int(sys.argv[2])

    run_lottery_client(proxy_ip, proxy_port)
