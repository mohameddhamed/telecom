# history_server_separate.py
import sys
import socket
import json
import os
from datetime import datetime

# --- Solves Task V.b (separate component) - receives logs from lottery server via UDP ---


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


def run_history_server(ip, port, log_file):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))
        print(f"History server listening on {ip}:{port} (UDP)")
        print(f"Logging to file: {log_file}")

        try:
            while True:
                data, server_addr = sock.recvfrom(1024)

                # Parse log message: "picked1:picked2:picked3:picked4:picked5:bet:drawn1:drawn2:drawn3:drawn4:drawn5:winnings"
                try:
                    parts = data.decode().split(":")
                    picked_numbers = [int(parts[i]) for i in range(5)]
                    bet_amount = int(parts[5])
                    drawn_numbers = [int(parts[i]) for i in range(6, 11)]
                    winnings = int(parts[11])

                    print(f"Received log from {server_addr}")
                    print(f"  Picked: {picked_numbers}, Bet: ${bet_amount}")
                    print(f"  Drawn: {drawn_numbers}, Winnings: ${winnings}")

                    # Create log entry
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "picked_numbers": picked_numbers,
                        "bet_amount": bet_amount,
                        "drawn_numbers": drawn_numbers,
                        "winnings": winnings,
                    }

                    append_to_json_log(log_file, log_entry)
                    print(f"Logged transaction to {log_file}")

                    # Send acknowledgment
                    sock.sendto(b"ACK", server_addr)

                except (ValueError, IndexError) as e:
                    print(f"Invalid log format from {server_addr}: {e}")

        except KeyboardInterrupt:
            print("\nHistory server shutting down.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python3 history_server_separate.py <listen_ip> <listen_port> <log_file>"
        )
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    log_file = sys.argv[3]

    run_history_server(listen_ip, listen_port, log_file)
