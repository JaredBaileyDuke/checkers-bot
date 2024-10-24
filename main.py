from src.board import Board
from src.piece import Piece

# Create 12 red pieces and 12 black pieces
red_pieces = [Piece('Red', i) for i in range(21, 33)] # Red locations 21-32
black_pieces = [Piece('Black', i) for i in range(1, 13)] # Black locations 1-12

# Initialize the game board
game_board = Board()

# Display the initial board
game_board.display_blank_board()

# Display current config of pieces
def display_pieces(red_pieces, black_pieces):
    print("Current Board:")
    print("   A B C D E F G H")
    print(" +----------------+")
    for row in range(8):
        print(f"{row}|", end="")
        for col in range(8, 0, -1):
            square = (row * 8) + col
            piece_found = False
            for piece in red_pieces:
                if piece.location == square:
                    print(f" {piece}", end="")
                    piece_found = True
                    break
            if not piece_found:
                for piece in black_pieces:
                    if piece.location == square:
                        print(f" {piece}", end="")
                        piece_found = True
                        break
            if not piece_found:
                print("  ", end="")

# Display the pieces on the current board
display_pieces(red_pieces, black_pieces)  # Call the function to display pieces