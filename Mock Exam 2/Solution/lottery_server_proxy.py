# history_server_proxy.py
import sys
import socket
import json
import os
from datetime import datetime

# --- Solves Task V.a (proxy mode) - uses UDP for history, TCP to forward to lottery ---


def append_to_json_log(log_file, entry):
    """Append entry to JSON log file"""
    try:
        # Read existing data
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                data = json.load(f)
        else:
            data = []

        # Append new entry
        data.append(entry)

        # Write back
        with open(log_file, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"Error writing to log file: {e}")


def run_history_proxy(ip, port, lottery_ip, lottery_port, log_file):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.bind((ip, port))
        print(f"History proxy server listening on {ip}:{port} (UDP)")
        print(
            f"Will forward requests to lottery server at {lottery_ip}:{lottery_port} (TCP)"
        )

        try:
            while True:
                data, client_addr = udp_sock.recvfrom(1024)

                # Parse client request: "num1:num2:num3:num4:num5:bet_amount"
                try:
                    parts = data.decode().split(":")
                    picked_numbers = [int(parts[i]) for i in range(5)]
                    bet_amount = int(parts[5])

                    print(
                        f"Received from {client_addr}: picked {picked_numbers}, bet ${bet_amount}"
                    )

                    # Forward to lottery server via TCP
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
                        tcp_sock.connect((lottery_ip, lottery_port))
                        tcp_sock.sendall(data)

                        # Receive response from lottery server
                        response = tcp_sock.recv(1024)
                        response_str = response.decode()

                        print(f"Received from lottery server: {response_str}")

                        # Parse lottery response
                        response_parts = response_str.split(":")
                        drawn_numbers = [int(response_parts[i]) for i in range(5)]
                        winnings = int(response_parts[5])

                        # Log the transaction
                        log_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "client": f"{client_addr[0]}:{client_addr[1]}",
                            "picked_numbers": picked_numbers,
                            "bet_amount": bet_amount,
                            "drawn_numbers": drawn_numbers,
                            "winnings": winnings,
                        }

                        append_to_json_log(log_file, log_entry)
                        print(f"Logged transaction to {log_file}")

                        # Forward response back to client
                        udp_sock.sendto(response, client_addr)
                        print(f"Forwarded result to {client_addr}")

                except (ValueError, IndexError) as e:
                    print(f"Invalid message format from {client_addr}: {e}")
                    udp_sock.sendto(b"ERROR:Invalid format", client_addr)
                except ConnectionRefusedError:
                    print("Could not connect to lottery server!")
                    udp_sock.sendto(b"ERROR:Lottery server unavailable", client_addr)

        except KeyboardInterrupt:
            print("\nHistory proxy server shutting down.")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python3 history_server_proxy.py <listen_ip> <listen_port> <lottery_ip> <lottery_port> <log_file>"
        )
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    lottery_ip = sys.argv[3]
    lottery_port = int(sys.argv[4])
    log_file = sys.argv[5]

    run_history_proxy(listen_ip, listen_port, lottery_ip, lottery_port, log_file)
