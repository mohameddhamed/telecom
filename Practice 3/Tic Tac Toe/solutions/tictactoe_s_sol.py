from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
import sys


class TicTacToeGame:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.players = []
        self.game_over = False
        self.winner = None

    def add_player(self, client_socket):
        if len(self.players) < 2:
            player_symbol = "X" if len(self.players) == 0 else "O"
            self.players.append({"socket": client_socket, "symbol": player_symbol})
            return player_symbol
        return None

    def make_move(self, x, y, player_symbol):
        if self.board[x][y] == " " and not self.game_over:
            self.board[x][y] = player_symbol
            if self.check_winner():
                self.game_over = True
                self.winner = player_symbol
            elif self.is_board_full():
                self.game_over = True
                self.winner = "Draw"
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True

        return False

    def is_board_full(self):
        for row in self.board:
            if " " in row:
                return False
        return True

    def get_board_string(self):
        board_str = ""
        for i, row in enumerate(self.board):
            board_str += " | ".join(row) + "\n"
            if i < 2:
                board_str += "---|---|---\n"
        return board_str


def handle_client(client_socket, game, player_symbol):
    try:
        # TODO: Send initial message to client - "START" for X player, "WAIT" for O player
        # (hint: use send() and encode())
        if player_symbol == "X":
            # Your code here
            client_socket.send("START".encode())
        else:
            # Your code here
            client_socket.send("WAIT".encode())

        while not game.game_over:
            if game.current_player == player_symbol:
                # It's this player's turn
                # TODO: Send "MOVE" message to client
                # Your code here
                client_socket.send("MOVE".encode())

                # TODO: Receive coordinates from client (hint: use recv() and decode())
                data = client_socket.recv(1024).decode()  # Your code here

                if not data:
                    break

                try:
                    x, y = map(int, data.split(","))
                    if 0 <= x <= 2 and 0 <= y <= 2:
                        if game.make_move(x, y, player_symbol):
                            # Send board state to both players
                            board_msg = f"BOARD\n{game.get_board_string()}"
                            for player in game.players:
                                # TODO: Send board message to each player
                                # Your code here
                                player["socket"].send(board_msg.encode())
                        else:
                            # TODO: Send "INVALID" message for invalid moves
                            # Your code here
                            client_socket.send("INVALID".encode())
                    else:
                        # TODO: Send "INVALID" message for out of bounds coordinates
                        # Your code here
                        client_socket.send("INVALID".encode())
                except ValueError:
                    # TODO: Send "INVALID" message for parsing errors
                    # Your code here
                    client_socket.send("INVALID".encode())
            else:
                # Wait for the other player's move
                # TODO: Send "WAIT" message to client
                # Your code here
                client_socket.send("WAIT".encode())
                threading.Event().wait(0.1)  # Small delay

        # Game is over, send final result
        if game.winner == player_symbol:
            # TODO: Send "WIN" message
            # Your code here
            client_socket.send("WIN".encode())
        elif game.winner == "Draw":
            # TODO: Send "DRAW" message
            # Your code here
            client_socket.send("DRAW".encode())
        else:
            # TODO: Send "LOSS" message
            # Your code here
            client_socket.send("LOSS".encode())

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # TODO: Close the client socket (hint: use close())
        # Your code here
        client_socket.close()


def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        return

    port = int(sys.argv[1])
    server_addr = ("", port)

    # TODO: Create a TCP socket and use it in a 'with' statement
    with socket(AF_INET, SOCK_STREAM) as server:  # Your code here
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # TODO: Bind the server to the server address
        # Your code here
        server.bind(server_addr)

        # TODO: Start listening for connections (accept 2 connections)
        # Your code here
        server.listen(2)

        print(f"Tic-Tac-Toe server listening on port {port}")

        while True:
            game = TicTacToeGame()
            print("Waiting for players...")

            # TODO: Accept first player connection
            client1, addr1 = server.accept()  # Your code here
            print(f"Player 1 connected: {addr1}")
            player1_symbol = game.add_player(client1)

            # TODO: Accept second player connection
            client2, addr2 = server.accept()  # Your code here
            print(f"Player 2 connected: {addr2}")
            player2_symbol = game.add_player(client2)

            print("Game starting!")

            # Start threads for both players
            thread1 = threading.Thread(
                target=handle_client, args=(client1, game, player1_symbol)
            )
            thread2 = threading.Thread(
                target=handle_client, args=(client2, game, player2_symbol)
            )

            thread1.start()
            thread2.start()

            thread1.join()
            thread2.join()

            print("Game ended!")


if __name__ == "__main__":
    main()
