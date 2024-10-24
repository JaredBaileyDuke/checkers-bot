from piece import Piece

class Board:
    def __init__(self):
        self.board = self.create_board()


    def create_board(self):
        """
        Initialize an 8x8 board with starting positions.
        Returns:
            A 2D list representing the board.
        """
        board = [[None for _ in range(8)] for _ in range(8)]
        # Place red pieces
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 != 0:
                    board[row][col] = Piece('Red', (row, col))
        # Place black pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    board[row][col] = Piece('Black', (row, col))
        return board

    def draw_board(self):
        """
        Display the board in the terminal.
        """
        print("  A B C D E F G H")
        for i in range(8):
            print(i + 1, end=" ")
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    if piece.get_king() == True:
                        print(piece.get_color[0].upper(), end=" ")
                    else:
                        print(piece.get_color[0].lower(), end=" ")
                else:
                    print(".", end=" ")
            print()

    def move_piece(self, piece, dest_row, dest_col):
        """
        Move a piece to a new location
        """
        # Check if the move is valid
        valid_moves = self.get_valid_moves(piece)

        # Check if the destination is in the list of valid moves
        if (dest_row, dest_col) not in valid_moves:
            print("Invalid move!")
            return
        
        # Move the piece
        piece.move(dest_row, dest_col)
        # Check for king promotion
        if (piece.color == 'Red' and dest_row == 7) or (piece.color == 'Black' and dest_row == 0):
            piece.promote_to_king()

    def get_valid_moves(self, piece):
        """
        Get a list of valid moves for a given piece.
        """
        valid_moves = []
        directions = piece.get_directions()
        row, col = piece.get_location()

        for direction in directions:
            new_row = row + direction[0]
            new_col = col + direction[1]

            # Check if the new position collides with the board boundaries

if __name__ == "__main__":
    game_board = Board()
    game_board.draw_board()  # Display the board
