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
    with # Your code here as client:
        
        # TODO: Connect to the server
        # Your code here
        
        print("Connected to Tic-Tac-Toe server!")
        
        # TODO: Receive initial message from server (hint: use recv() and decode())
        initial_msg = # Your code here
        
        if initial_msg == "START":
            print("You are player X (starting player)")
            is_starting_player = True
        else:
            print("You are player O (waiting player)")
            is_starting_player = False
        
        game_running = True
        while game_running:
            try:
                # TODO: Receive message from server
                message = # Your code here
                
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
                            x, y = map(int, move.split(','))
                            if 0 <= x <= 2 and 0 <= y <= 2:
                                # TODO: Send the move to the server (hint: use send() and encode())
                                # Your code here
                                break
                            else:
                                print("Coordinates must be between 0-2!")
                        except ValueError:
                            print("Please enter coordinates in format: x,y")
                
                elif message == "WAIT":
                    print("Waiting for other player's move...")
                
                elif message == "INVALID":
                    print("Invalid move! That position might be taken. Try again.")
                
                elif message.startswith("BOARD"):
                    print("\nCurrent board:")
                    board_lines = message.split('\n')[1:]  # Skip "BOARD" line
                    for line in board_lines:
                        print(line)
                
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
                    print(f"Unknown message: {message}")
                    
            except Exception as e:
                print(f"Error: {e}")
                break
        
        print("Game ended. Goodbye!")

if __name__ == "__main__":
    main()