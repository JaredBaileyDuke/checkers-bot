# I am building a checkers game using Python, but not pygame
# I will create a class for the game board and a class for the pieces
from src.board import Board



class Piece:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.color[0].upper()  # Return the first letter of the color
    
# Example usage
if __name__ == "__main__":
    game_board = Board()
    game_board.display_board()