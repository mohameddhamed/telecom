from socket import socket, AF_INET, SOCK_STREAM
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    server_addr = (host, port)

    # TODO: Create a TCP socket and use it in a 'with' statement
    with socket(AF_INET, SOCK_STREAM) as client:  # Your code here

        # TODO: Connect to the server
        # Your code here
        client.connect(server_addr)

        print("Connected to Tic-Tac-Toe server!")

        # TODO: Receive initial message from server (hint: use recv() and decode())
        initial_msg = client.recv(1024).decode()  # Your code here

        if initial_msg == "START":
            print("You are player X (starting player)")
        else:
            print("You are player O (waiting player)")

        game_running = True
        while game_running:
            try:
                # TODO: Receive message from server
                message = client.recv(1024).decode()  # Your code here

                if not message:
                    print("Connection to server lost.")
                    break

                if message == "MOVE":
                    print("\nYour turn! Enter coordinates (x,y) where x,y are 0-2:")
                    print("Board positions:")
                    print("0,0 | 0,1 | 0,2")
                    print("----|----|----")
                    print("1,0 | 1,1 | 1,2")
                    print("----|----|----")
                    print("2,0 | 2,1 | 2,2")

                    while True:
                        try:
                            move = input("Enter your move (x,y): ").strip()
                            x, y = map(int, move.split(","))
                            if 0 <= x <= 2 and 0 <= y <= 2:
                                # TODO: Send the move to the server (hint: use send() and encode())
                                # Your code here
                                client.send(move.encode())
                                break
                            else:
                                print("Coordinates must be between 0-2!")
                        except ValueError:
                            print("Please enter coordinates in format: x,y")

                elif message == "WAIT":
                    print("Waiting for other player's move...")

                elif message == "INVALID":
                    print(
                        "Invalid move! That position might be taken or coordinates are wrong. Try again."
                    )

                elif message.startswith("BOARD"):
                    print("\nCurrent board:")
                    board_str = message.split("\n", 1)[1]  # Skip "BOARD" line
                    print(board_str)

                elif message == "WIN":
                    print("\n🎉 Congratulations! You won! 🎉")
                    game_running = False

                elif message == "LOSS":
                    print("\n😞 You lost! Better luck next time!")
                    game_running = False

                elif message == "DRAW":
                    print("\n🤝 It's a draw! Good game!")
                    game_running = False

                else:
                    # This handles the initial START/WAIT message which doesn't require a response
                    if message not in ["START", "WAIT"]:
                        print(f"Unknown message: {message}")

            except ConnectionAbortedError:
                print("Connection was aborted.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        print("Game ended. Goodbye!")


if __name__ == "__main__":
    main()
