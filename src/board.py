from piece import Piece

class Board:
    def __init__(self):
        """
        Initialize the board with pieces in starting positions
        """
        self.board, self.pieces = self.create_board()
        self.red_count = 12
        self.black_count = 12
        self.store_piece_locations()
        

    def create_board(self):
        """
        Initialize an 8x8 board with starting positions.
        Returns:
            A 2D list representing the board.
        """
        board = [[None for _ in range(8)] for _ in range(8)]
        pieces = []
        # Place red pieces
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 != 0:
                    board[row][col] = Piece('red', (row, col))
                    pieces.append(board[row][col])           
        # Place black pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    board[row][col] = Piece('black', (row, col))
                    pieces.append(board[row][col])

        return board, pieces
    
    def store_piece_locations(self):
        """
        Store piece locations in a list for easy access
        """
        self.piece_locations = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None:
                    self.piece_locations.append((row, col))

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
        jumpped = False

        # Check if the move is a jump
        for jump in piece.get_potential_jump_directions():
            if (dest_row, dest_col) == (piece.get_location()[0] + jump[0], piece.get_location()[1] + jump[1]):
                # Jump over the opponent's piece
                curr_row, curr_col = piece.get_location()
                over_row = (curr_row + dest_row) // 2
                over_col = (curr_col + dest_col) // 2
                print("Jumped over", self.get_piece(over_row, over_col))
                self.remove_piece(self.get_piece(over_row, over_col), remove_from_list=True)
                # Update the count of pieces
                if piece.color == 'red':
                    self.black_count -= 1
                else:
                    self.red_count -= 1
                jumpped = True

        # Move the piece
        self.remove_piece(piece)
        piece.move(dest_row, dest_col)
        self.board[dest_row][dest_col] = piece

        # Check for king promotion
        if (piece.color == 'red' and dest_row == 7) or (piece.color == 'black' and dest_row == 0):
            piece.promote_to_king()

        #update piece locations
        self.store_piece_locations()

        #check for extra jumps if a jump was made
        if jumpped:
            valid_jumps = self.find_valid_jumps(piece)
            if len(valid_jumps) > 0:
                piece.extra_jump = True
            else:
                piece.extra_jump = False

    def find_valid_moves_and_jumps(self, piece, only_jumps=False):
        """
        Get a list of all valid moves and jumps for a given piece.
        """
        if only_jumps:
            return self.find_valid_jumps(piece)
        
        valid_moves = self.find_valid_moves(piece)
        valid_jumps = self.find_valid_jumps(piece)

        return valid_moves + valid_jumps
    
    def find_valid_moves(self, piece):
        """
        Get a list of valid moves for a given piece.
        """
        valid_moves = []
        curr_row, curr_col = piece.get_location()

        # Get potential move directions
        move_directions = piece.get_potential_move_directions()

        # Add potential moves to valid moves, including adding to current position
        for direction in move_directions:
            new_row = curr_row + direction[0]
            new_col = curr_col + direction[1]
            valid_moves.append((new_row, new_col))

        i = 0
        # see if the location is empty
        while i < len(valid_moves):
            if valid_moves[i] in self.piece_locations:
                valid_moves.remove(valid_moves[i])
                i -= 1
                if i >= len(valid_moves):
                    break
            i += 1
                
        return valid_moves
    
    def find_valid_jumps(self, piece):
        """
        Get a list of valid jumps for a given piece.
        """
        valid_jumps = []
        curr_row, curr_col = piece.get_location()

        # Get potential move directions
        jump_directions = piece.get_potential_jump_directions()

        # Add potential moves to valid moves, including adding to current position
        for direction in jump_directions:
            new_row = curr_row + direction[0]
            new_col = curr_col + direction[1]
            valid_jumps.append((new_row, new_col))

        i = 0
        # see if the location is empty
        while i < len(valid_jumps):
            if valid_jumps[i] in self.piece_locations:
                valid_jumps.remove(valid_jumps[i])
                i -= 1
                if i >= len(valid_jumps):
                    break
            i += 1
        
        i = 0
        # search other pieces to see if jump is valid
        while i < len(valid_jumps):
            if not self.is_valid_jump(piece, valid_jumps[i][0], valid_jumps[i][1]):
                valid_jumps.remove(valid_jumps[i])
                i -= 1
                if i >= len(valid_jumps):
                    break
            i += 1

        return valid_jumps

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
    
    def find_color_pieces(self, color):
        """
        Get a list of all pieces for a given color.
        """
        color_pieces = []
        for piece in self.pieces:
            if piece.color == color:
                color_pieces.append(piece)
        return color_pieces

    def remove_piece(self, piece, remove_from_list=False):
        piece_location = piece.get_location()
        self.board[piece_location[0]][piece_location[1]] = None
        if remove_from_list:
            self.pieces.remove(piece)

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def print_pieces(self):
        for piece in self.pieces:
            #print each piece string without a newline
            print(piece, end=" ")
        print()

if __name__ == "__main__":
    game_board = Board()
    game_board.draw_board()  # Display the board
    game_board.store_piece_locations()
    print(game_board.pieces) # piece list
