from board import Board
import random

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'red'  # Starting player
        self.valid_moves = {}

    def switch_turn(self):
        if self.turn == 'red':
            self.turn = 'black'
        else:
            self.turn = 'red'

    def ai_turn(self, restricted_jump=None):
        """
        AI turn logic
        """
        self.board.draw_board()
        print(f"{self.turn.capitalize()}'s turn")

        # Get the best move for the AI
        piece, dest = self.get_best_move(self.turn, restricted_jump)
        start_row, start_col = piece.location
        dest_row, dest_col = dest

        # Move the piece
        self.board.move_piece(piece, dest_row, dest_col)
        print("Moved " + piece.color + " piece from " + chr(start_col + ord('A')) + str(start_row + 1) + " to " + chr(dest_col + ord('A')) + str(dest_row + 1))

        if piece.extra_jump:
            print("Extra jump available!")
            self.ai_turn(restricted_jump=(dest_row, dest_col))

    def user_turn(self, show_board=True, restricted_jump=None):
        """
        User turn logic
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

        # Get the piece to move
        piece = self.board.get_piece(start_row, start_col)

        # Move the piece
        self.board.move_piece(piece, dest_row, dest_col)
        print("Moved " + piece.color + " piece from " + start + " to " + end)

        if piece.extra_jump:
            print("Extra jump available!")
            self.user_turn(restricted_jump=(dest_row, dest_col))

    def check_winner(self):
        red_pieces = 0
        black_pieces = 0
        
        for row in self.board.board:
            for piece in row:
                if piece is not None:
                    if piece.color == 'red':
                        red_pieces += 1
                    else:
                        black_pieces += 1
        if red_pieces == 0:
            print("Black wins!")
            return True
        elif black_pieces == 0:
            print("Red wins!")
            return True
        return False
    
    def get_best_move(self, color, restricted_jump=None):
        """
        Get the best move for the AI
        """
        if restricted_jump is not None:
            valid_moves = self.board.find_valid_moves_and_jumps(self.board.get_piece(restricted_jump[0], restricted_jump[1]), only_jumps=True)
            return valid_moves[0]
        
        valid_moves = []
        piece = None

        while len(valid_moves) == 0:
            #choose a random piece for now
            valid_pieces = self.board.find_color_pieces(color)
            random.shuffle(valid_pieces)
            piece = valid_pieces[0]
            valid_moves = self.board.find_valid_moves_and_jumps(piece)

        random.shuffle(valid_moves)
        return piece, valid_moves[0]
    
    def play(self):
        while True:
            if self.turn == 'red':
                self.user_turn()
            else:
                self.ai_turn()
                # self.user_turn()
            if self.check_winner():
                break
            self.switch_turn()

if __name__ == "__main__":
    game = Game()
    game.play()