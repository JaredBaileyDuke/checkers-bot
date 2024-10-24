class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = []
        for row in range(8):
            board.append([None] * 8)
        return board

    def display_board(self):
        for row in self.board:
            print(" ".join([str(piece) if piece else '.' for piece in row]))