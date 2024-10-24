class Board:
    def __init__(self):
        self.board = self.create_board()


    def create_board(self):
        """
        Create an 8x8 board
        - '#' for empty squares
        - ' ' for squares that cannot be moved to.
        """
        board = []
        square_notation = 1
        row_counter = 0
        for row in range(8):
            # Create a new row
            new_row = []
            for col in range(8):
                if (col + row) % 2 == 0:
                    new_row.append(0)
                else:
                    new_row.append(square_notation)
                    square_notation += 1
            board.append(new_row)
            row_counter += 1

        return board

    def display_blank_board(self):
        print("Blank Board:")
        print("   A B C D E F G H")
        print(" +----------------+")
        for i, row in enumerate(self.board):
            print(f"{7 - i + 1}|", end="")
            for square in row:
                if square == 0:
                    print("  ", end="")
                elif len(str(square)) == 1:
                    print(f" {square}", end="")
                else:
                    print(f"{square}", end="")
            print("|")
        
        
# Example usage
if __name__ == "__main__":
    game_board = Board()
    game_board.display_blank_board()