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
                    board[row][col] = Piece('red', (row, col))
        # Place black pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    board[row][col] = Piece('black', (row, col))

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
        Assuming the move to be made is already validated
        """

        # Check if the move is a jump
        for jump in piece.get_potential_jump_directions():
            if (dest_row, dest_col) == (piece.get_location()[0] + jump[0], piece.get_location()[1] + jump[1]):
                # Jump over the opponent's piece
                curr_row, curr_col = piece.get_location()
                over_row = (curr_row + dest_row) // 2
                over_col = (curr_col + dest_col) // 2
                print("Jumped over", self.get_piece(over_row, over_col))
                self.remove_piece(self.get_piece(over_row, over_col))

        # Move the piece
        self.remove_piece(piece)
        piece.move(dest_row, dest_col)
        self.board[dest_row][dest_col] = piece

        # Check for king promotion
        if (piece.color == 'red' and dest_row == 7) or (piece.color == 'black' and dest_row == 0):
            piece.promote_to_king()

        #update piece locations
        self.store_piece_locations()

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

        # see if the location is empty
        for move in valid_moves:
            if move in self.pieces:
                valid_moves.remove(move)
        
        # search other pieces to see if jump is valid
        for potential_jump in valid_jumps:
            jump_row = potential_jump[0]
            jump_col = potential_jump[1]
            # Check if there is an opponent's piece to jump over
            if not self.is_valid_jump(piece, jump_row, jump_col):
                valid_jumps.remove(potential_jump)

        return valid_moves + valid_jumps

    def is_valid_jump(self, piece, jump_row, jump_col):
        """
        Check if a jump is valid by verifying if there is an opponent's piece to jump over
        Also checks if the destination is valid
        """
        #If there is a piece at the destination, return False
        if self.get_piece(jump_row, jump_col) is not None:
            return False
        
        curr_row, curr_col = piece.get_location()
        # Calculate the row and column of the piece being jumped over
        over_row = (curr_row + jump_row) // 2
        over_col = (curr_col + jump_col) // 2

        # Check if the piece being jumped over is an opponent's piece
        if self.get_piece(over_row, over_col) is not None:
            return self.get_piece(over_row, over_col).color != piece.color #check if the piece is an opponent's piece
            
        return False   
    
    def remove_piece(self, piece):
        piece_location = piece.get_location()
        self.board[piece_location[0]][piece_location[1]] = None

    def get_piece(self, row, col):
        return self.board[row][col]


if __name__ == "__main__":
    game_board = Board()
    game_board.draw_board()  # Display the board
    game_board.store_piece_locations()
    print(game_board.pieces) # piece list
