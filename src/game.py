from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'red'  # Starting player
        self.valid_moves = {}

    def switch_turn(self):
        self.turn = 'black' if self.turn == 'red' else 'red'

    def user_turn(self):
        """
        User turn logic
        """

        while True:
            self.board.draw_board()
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

                #Make sure piece exists in the start location
                if self.board.get_piece(start_row, start_col) is None:
                    print("No piece at that location!")
                    continue

                #Make sure piece is the correct color
                if self.board.get_piece(start_row, start_col).color != self.turn:
                    print("Wrong color piece! It's " + self.turn + "'s turn.")
                    print("You are trying to move a " + self.board.get_piece(start_row, start_col).color + " piece.")
                    continue

                #Make sure destination is empty
                if self.board.get_piece(dest_row, dest_col) is not None:
                    print("Destination is not empty!")
                    continue

                #Make sure move is valid
                valid_moves = self.board.find_valid_moves_and_jumps(self.board.get_piece(start_row, start_col))
                print(self.board.get_piece(start_row, start_col))
                print(valid_moves)
                if (dest_row, dest_col) not in valid_moves:
                    print("Invalid move!")
                    continue

                break

            # Get the piece to move
            piece = self.board.get_piece(start_row, start_col)

            # Move the piece
            self.board.move_piece(piece, dest_row, dest_col)

    def check_winner(self):
        red_pieces = 0
        black_pieces = 0
        
        for row in self.board.board:
            for piece in row:
                if piece is not None:
                    if piece.color == 'Red':
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
    
    def play(self):
        while True:
            self.user_turn()
            if self.check_winner():
                break
            self.switch_turn()

if __name__ == "__main__":
    game = Game()
    game.play()