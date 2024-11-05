from piece import Piece

class Board:
    def __init__(self):
        """
        Initialize the board with pieces in starting positions
        """
        self.board = self.create_board()
        self.store_piece_locations()

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
    
    def store_piece_locations(self):
        """
        Store piece locations in a list for easy access
        """
        self.pieces = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    piece_location = piece.get_location()
                    self.pieces.append(piece_location)

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
                        print(piece.get_color()[0].upper(), end=" ")
                    else:
                        print(piece.get_color()[0].lower(), end=" ")
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

    def find_valid_moves_and_jumps(self, piece):
        """
        Get a list of valid moves for a given piece.
        """
        valid_moves = []
        valid_jumps = []
        curr_row, curr_col = piece.get_location()

        # Get potential move directions
        move_directions = piece.get_potential_move_directions()
        jump_directions = piece.get_potential_jump_directions()

        # Add potential moves to valid moves, including adding to current position
        for direction in move_directions:
            new_row = curr_row + direction[0]
            new_col = curr_col + direction[1]
            valid_moves.append((new_row, new_col))
        for direction in jump_directions:
            new_row = curr_row + direction[0]
            new_col = curr_col + direction[1]
            valid_jumps.append((new_row, new_col))

        # TODO: Make is_collision method to check if the move or jump is a collision with another piece
        # search other pieces to see if the move will collide
        for other_piece in self.board:
            other_piece_location = other_piece.get_location()
            # remove the location of the other piece from valid moves
            if other_piece_location in valid_moves:
                valid_moves.remove(other_piece_location)
            # remove the location of the other piece from valid jumps
            if other_piece_location in valid_jumps:
                valid_jumps.remove(other_piece_location)

        # search other pieces to see if jump is valid
        for potential_jump in valid_jumps:
            jump_row = potential_jump[0]
            jump_col = potential_jump[1]
            # Check if there is an opponent's piece to jump over
            if self.is_valid_jump(piece, jump_row, jump_col):
                valid_jumps.append(potential_jump)

        return valid_moves + valid_jumps

    def is_valid_jump(self, piece, jump_row, jump_col):
        """
        Check if a jump is valid by verifying if there is an opponent's piece to jump over
        Does not check if the destination is valid
        """
        curr_row, curr_col = piece.get_location()
        # Calculate the row and column of the piece being jumped over
        over_row = (curr_row + jump_row) // 2
        over_col = (curr_col + jump_col) // 2

        # Check if the piece being jumped over is an opponent's piece
        for other_piece in self.board:
            if other_piece.get_location() == (over_row, over_col):
                return other_piece.color != piece.color # Return True if it's an opponent's piece
        return False   
    
    def remove_piece(self, piece):
        self.board[piece.location] = None


if __name__ == "__main__":
    game_board = Board()
    game_board.draw_board()  # Display the board
    game_board.store_piece_locations()
    print(game_board.pieces) # piece list
