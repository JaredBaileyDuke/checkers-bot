import board

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
            # Get user input for piece selection and move
            user_input = input("Enter your move (e.g., 'A3 B4'): ")

            # Parse user input
            while True:
                try:
                    start, end = user_input.split()
                    start_row, start_col = int(start[1]) - 1, ord(start[0].upper()) - ord('A')
                    end_row, end_col = int(end[1]) - 1, ord(end[0].upper()) - ord('A')  
                except (ValueError, IndexError):
                    print("Invalid input. Please enter in the format 'A3 B4'.")
                    continue
                break
            # TODO: Make sure to validate input and handle moves

            # Get the piece to move
            piece = self.board.board[start_row][start_col]

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
