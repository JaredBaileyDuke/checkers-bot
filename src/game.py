from board import Board
import random
from time import sleep

class Game:
    def __init__(self):
        """
        Set up the game
        """
        self.board = Board()
        self.turn = 'red'  # Starting player
        self.valid_moves = {}

    def switch_turn(self):
        """
        Switch the turn to the other player
        """
        if self.turn == 'red':
            self.turn = 'black'
        else:
            self.turn = 'red'

    def user_turn(self, show_board=True, restricted_jump=None):
        """
        User turn logic

        Args:
            show_board, bool: Whether to show the board
            restricted_jump, tuple: piece location - since a jump occurred, the user must continue jumping with the same piece
        """
        if show_board: self.board.draw_board()
        print(f"{self.turn.capitalize()}'s turn")

        #Get and parse user input
        while True:
            # Get user input for piece selection and move
            user_input = input("Enter your move (e.g., 'A3 B4'): ")

            try:
                start, end = user_input.split()
                start_row, start_col = int(start[1]) - 1, ord(start[0].upper()) - ord('A')
                dest_row, dest_col = int(end[1]) - 1, ord(end[0].upper()) - ord('A')  
            except (ValueError, IndexError):
                print("Invalid input. Please enter in the format 'A3 B4'.")
                continue

            #if a jump is restricted, make sure the user jumps with that piece
            if restricted_jump is not None:
                if (start_row, start_col) != restricted_jump:
                    print("You must jump with the piece at", chr(restricted_jump[1] + ord('A')) + str(restricted_jump[0] + 1))
                    continue

            #Make sure piece exists in the start location
            if self.board.get_piece(start_row, start_col) is None:
                print("No piece at that location!")
                continue

            #Make sure piece is the correct color
            if self.board.get_piece(start_row, start_col).color != self.turn:
                print("Wrong color piece! It's " + self.turn + "'s turn.")
                print("You are trying to move a " + self.board.get_piece(start_row, start_col).color + " piece.")
                continue

            #Make sure move is valid
            valid_moves = self.board.find_valid_moves_and_jumps(self.board.get_piece(start_row, start_col), restricted_jump is not None)
            if (dest_row, dest_col) not in valid_moves:
                print("Invalid move for piece", self.board.get_piece(start_row, start_col))
                print("Valid moves are: " + str(valid_moves))
                continue

            break

    def ai_turn(self, difficulty="Random", restricted_jump=None):
        """
        AI turn logic with difficulty setting
        - Random: Choose a random move

        Args:
            restricted_jump, tuple: since a jump occurred, the AI must continue jumping with the same piece
        """
        # Show the board and print the current player's turn
        self.board.draw_board()
        print(f"{self.turn.capitalize()}'s turn")

        # Get the best move for the AI
        if difficulty == "Random":
            self.make_random_move()
        elif difficulty == "Minimax":
            self.make_minimax_move()
        elif difficulty == "Prefer Jumps":
            self.make_prefer_jumps()

    def make_minimax_move(self, restricted_jump=None):
        """
        Make a move for the AI using the minimax algorithm

        Args:
            restricted_jump, tuple: location - since a jump occurred, the AI must continue jumping with the same piece
        """
        pass

    def make_prefer_jumps(self, restricted_jump=None):
        """
        Make a move for the AI that prefers jumps

        Args:
            restricted_jump, tuple: location - since a jump occurred, the AI must continue jumping with the same piece
        """
        pass

    def make_random_move(self, restricted_jump=None):
        """
        Make a random move for the AI

        Args:
            restricted_jump, tuple: location - since a jump occurred, the AI must continue jumping with the same piece
        """
        # If no restricted jump, choose a random piece
        if restricted_jump is None: 
            # Get all pieces of the given color
            valid_pieces = self.board.find_color_pieces(self.turn)
            valid_moves = []

            # Choose a random piece
            while len(valid_moves) == 0: # If no valid moves, choose a different piece randomly
                # Choose a piece randomly
                random.shuffle(valid_pieces)
                piece = valid_pieces[0]

                # Get random moves
                valid_moves = self.board.find_valid_moves_and_jumps(piece)

            # Choose a random move
            random.shuffle(valid_moves)
            dest = valid_moves[0]

        # If a restricted jump, choose the piece that must jump
        else: 
            temp_piece = self.board.get_piece(restricted_jump[0], restricted_jump[1]) # Get the piece that must jump
            valid_moves = self.board.find_valid_moves_and_jumps(temp_piece, only_jumps=True) # Get all valid jumps for the piece
            piece, dest =  temp_piece, valid_moves[0]

        # Get piece location, and destination location
        start_row, start_col = piece.get_location()
        dest_row, dest_col = dest

        # Move the piece
        self.board.move_piece(piece, dest_row, dest_col)
        print("Moved " + piece.color + " piece from " + chr(start_col + ord('A')) + str(start_row + 1) + " to " + chr(dest_col + ord('A')) + str(dest_row + 1))

        # Check if the piece can make an extra jump
        if piece.extra_jump:
            print("Extra jump available!")
            self.make_random_move(restricted_jump=(dest_row, dest_col))

    def check_winner(self):
        """
        Check if the game is over and print the winner

        Returns:
            bool: True if the game is over, False otherwise
        """
        red_pieces = self.board.red_count
        black_pieces = self.board.black_count

        #print the counts of each color
        print("Red pieces:", red_pieces)
        print("Black pieces:", black_pieces)
    
        if red_pieces == 0:
            self.board.draw_board()
            print("Black wins!")
            return True
        elif black_pieces == 0:
            self.board.draw_board()
            print("Red wins!")
            return True
        return False
    
    def play(self):
        """
        Game loop
        """
        while True:
            if self.turn == 'red':
                self.ai_turn(difficulty="Random")
                # self.user_turn()
            else:
                self.ai_turn(difficulty="Random")
                # self.user_turn()
            if self.check_winner():
                break
            self.switch_turn()
            self.board.print_pieces()
            sleep(1)

if __name__ == "__main__":
    game = Game()
    game.play()