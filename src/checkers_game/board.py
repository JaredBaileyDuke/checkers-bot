from .piece import Piece

class Board:
    def __init__(self, mode='classic', layout=['RB1', 'RD1', 'BA8', 'BC8K']):
        """
        Initialize the board with pieces in starting positions
        """
        self.red_count = 0
        self.black_count = 0
        self.red_king_count = 0
        self.black_king_count = 0
        self.board, self.pieces = self.create_board(layout=mode, custom_layout=layout)
        self.store_piece_locations()
        
    def create_board(self, layout='classic', custom_layout=['RB1', 'RD1', 'BA8', 'BC8K']):
        """
        Initialize an 8x8 board with starting positions
    
        Returns:
            board, list of lists: A 2D matrix representing the board, contains pieces
            pieces, list: A list of all pieces on the board
        """
        board: list[list[None | Piece]] = [[None for _ in range(8)] for _ in range(8)]
        pieces: list[Piece] = []
        if layout == 'classic':
            # Place red pieces
            for row in range(3):
                for col in range(8):
                    if (row + col) % 2 != 0:
                        board[row][col] = Piece('red', (row, col))
                        pieces.append(board[row][col])
                        self.red_count += 1          
            # Place black pieces
            for row in range(5, 8):
                for col in range(8):
                    if (row + col) % 2 != 0:
                        board[row][col] = Piece('black', (row, col))
                        pieces.append(board[row][col])
                        self.black_count += 1
        elif layout == 'empty':
            pass
        elif layout == 'custom':
            for piece_str in custom_layout:
                color = piece_str[0].lower()
                row = int(piece_str[2])-1
                col = ord(piece_str[1].upper()) - 65
                if color == 'r':
                    color = 'red'
                    self.red_count += 1
                elif color == 'b':
                    color = 'black'
                    self.black_count += 1
                piece = Piece(color, (row, col))
                try: 
                    if piece_str[3] == 'K':
                        piece.promote_to_king()
                        piece.crown()
                        if color == 'red': self.red_king_count += 1
                        if color == 'black': self.black_king_count += 1
                except IndexError:
                    pass
                board[row][col] = piece
                pieces.append(piece)
        else:
            raise ValueError("Invalid board layout")
        return board, pieces
    
    def store_piece_locations(self):
        """
        Store piece locations in a list for easy access, especially by AI
        """
        self.piece_locations = []
        num_pieces = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] is not None:
                    # print("Piece found: ", self.get_piece(row, col))
                    self.piece_locations.append((row, col))
                    num_pieces += 1
                    if self.get_piece(row, col) not in self.pieces:
                        print("Piece not found in pieces list")
                        print("Piece: ", self.get_piece(row, col))
                        self.print_pieces()
                        #throw an error
                        raise ValueError("Piece not found in pieces list")
        
        #check to see if the piece list is the same as the piece locations
        if len(self.piece_locations) != len(self.pieces):
            print("Piece locations and pieces list lengths are not the same")
            print("Piece Locations: ", self.piece_locations)
            print("Pieces: ")
            self.print_pieces()
            raise ValueError("Piece locations and pieces list lengths are not the same, piece locations: " + str(len(self.piece_locations)) + " pieces: " + str(len(self.pieces)))

    def draw_board(self):
        """
        Display the board in the terminal
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

        Args:
            piece, Piece: The piece to move
            dest_row, int: The row to move the piece to
            dest_col, int: The column to move the piece to
        """
        #make sure the piece is in the list of pieces
        flag = False
        #make sure the piece is in the list of pieces
        for other_piece in self.pieces:
            if other_piece == piece:
                flag = True
                #check if they are the same piece object
                if other_piece is not piece:
                    #set the piece to the piece in the list
                    # print("Piece object mismatch")
                    piece = other_piece
                break

        if not flag:
            print("Piece: ", piece)
            print("Piece List: ")
            self.print_pieces()
            print("attempting to move to ", dest_row, dest_col)
            raise ValueError("Tried to move a piece not found in list of pieces")
            
        jumped = False

        # Check if the move is a jump
        jump_directions = piece.get_potential_jump_directions()
        for jump in jump_directions:
            if (dest_row, dest_col) == (piece.get_location()[0] + jump[0], piece.get_location()[1] + jump[1]):
                # Jump over the opponent's piece
                curr_row, curr_col = piece.get_location()
                over_row = (curr_row + dest_row) // 2
                over_col = (curr_col + dest_col) // 2
                # print("jump_directions: ", jump_directions)
                # print(piece, "attempting to jump over", over_row, over_col)
                # print("Jumped over", self.get_piece(over_row, over_col))
                self.remove_piece(self.get_piece(over_row, over_col), remove_from_list=True)

                # Update the count of pieces
                if piece.color == 'red':
                    self.black_count -= 1
                else:
                    self.red_count -= 1

                jumped = True

        # Move the piece
        self.remove_piece(piece)
        piece.move(dest_row, dest_col)
        self.board[dest_row][dest_col] = piece

        # Check for king promotion
        if (piece.color == 'red' and dest_row == 7) or (piece.color == 'black' and dest_row == 0):
            #if it is not already a king update king counts
            if not piece.get_king():
                if piece.color == 'red': self.red_king_count += 1
                if piece.color == 'black': self.black_king_count += 1
                piece.promote_to_king()

        # update piece locations
        self.store_piece_locations()
        # print("Finished moving piece and storing piece locations")

        # check for extra jumps if a jump was made
        if jumped:
            valid_jumps = self.find_valid_jumps(piece)
            if len(valid_jumps) > 0:
                piece.extra_jump = True
            else:
                piece.extra_jump = False
        else:
            piece.extra_jump = False
        
        return piece
    
    def undo_move(self, piece, dest_row, dest_col):
        """
        Undo a move made by a piece

        Args:
            piece, Piece: The piece to undo the move for
            dest_row, int: The row the piece will be moved back to
            dest_col, int: The column the piece will be moved back to
        """
        flag = False
        #make sure the piece is in the list of pieces
        for other_piece in self.pieces:
            if other_piece == piece:
                flag = True
                #check if they are the same piece object
                if other_piece is not piece:
                    #set the piece to the piece in the list
                    # print("Piece object mismatch")
                    piece = other_piece
                break

        if not flag:
            print("Piece not found in list of pieces")
            print("Piece: ", piece)
            print("Piece List: ")
            self.print_pieces()
            raise ValueError("Piece not found in list of pieces")
                
        #if the piece was promoted to a king, demote it
        if piece.get_king():
            piece.demote_from_king()

        old_location = piece.get_location()

        # Check if a piece was jumped over
        if abs(old_location[0] - dest_row) == 2:
            curr_row, curr_col = piece.get_location()
            over_row = (curr_row + dest_row) // 2
            over_col = (curr_col + dest_col) // 2
            self.add_piece(Piece('black' if piece.color == 'red' else 'red', (over_row, over_col)))
        
        #move it back to the original location
        self.remove_piece(piece)
        piece.move(dest_row, dest_col)
        self.board[dest_row][dest_col] = piece
        # print("Moved back: ", piece, " from ", old_location, " to ", piece.get_location())

        # Update piece locations
        self.store_piece_locations()
        # print("Finished undoing move")

        return piece

    def find_valid_moves_and_jumps(self, piece, only_jumps=False):
        """
        Get a list of all valid moves and jumps for a given piece

        Args:
            piece, Piece: The piece to find valid moves and jumps for
            only_jumps, bool: Whether to only find jumps
        """
        # self.store_piece_locations()
        # Get valid jumps only
        if only_jumps:
            return self.find_valid_jumps(piece)
        
        # Get valid moves and jumps
        valid_moves = self.find_valid_moves(piece)
        valid_jumps = self.find_valid_jumps(piece)

        return valid_moves + valid_jumps
    
    def find_valid_moves(self, piece):
        """
        Get a list of valid moves for a given piece

        Args:
            piece, Piece: The piece to find valid moves for

        Returns:
            valid_moves, list of tuples: A list of valid moves for the given piece
        """        
        valid_moves: list[tuple[int, int]] = []
        curr_row, curr_col = piece.get_location()

        # Get potential move directions
        move_directions = piece.get_potential_move_directions()

        # Add potential moves to valid moves
        for direction in move_directions:
            new_row = curr_row + direction[0]
            new_col = curr_col + direction[1]
            valid_moves.append((new_row, new_col))

        # Remove invalid moves
        # see if the location being moved to is empty, if not remove it
        i = 0
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
        Get a list of valid jumps for a given piece

        Args:
            piece, Piece: The piece to find valid jumps for

        Returns:
            valid_jumps, list of tuples: A list of valid jumps for the given piece
        """
        valid_jumps: list[tuple[int, int]] = []
        curr_row, curr_col = piece.get_location()

        # Get potential move directions
        jump_directions = piece.get_potential_jump_directions()

        # Add potential moves to valid moves
        for direction in jump_directions:
            new_row = curr_row + direction[0]
            new_col = curr_col + direction[1]
            valid_jumps.append((new_row, new_col))

        # Remove invalid jumps
        # see if the location being jumped to is empty, if not remove it
        i = 0
        while i < len(valid_jumps):
            if valid_jumps[i] in self.piece_locations:
                valid_jumps.remove(valid_jumps[i])
                i -= 1
                if i >= len(valid_jumps):
                    break
            i += 1
        
        # search other pieces to see if jump is valid
        i = 0
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

        Args:   
            piece, Piece: The piece making the jump
            jump_row, int: The row to jump to
            jump_col, int: The column to jump to

        Returns:
            bool: Whether the jump is valid
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
            # print("Jumping over: ", self.get_piece(over_row, over_col))
            return self.get_piece(over_row, over_col).color != piece.color #check if the piece is an opponent's piece
            
        return False   
    
    def find_color_pieces(self, color):
        """
        Get a list of all pieces for a given color

        Args:
            color, str: The color of the pieces to get

        Returns:
            color_pieces, list: A list of all pieces for the given color
        """
        color = color.lower() # Ensure the color is lowercase
        color_pieces = []

        for piece in self.pieces:
            if piece.color == color:
                color_pieces.append(piece)

        return color_pieces
    
    def remove_all_pieces(self):
        """
        Remove all pieces from the board
        """
        for piece in self.pieces:
            self.remove_piece(piece, remove_from_list=True)
        self.pieces = []
        self.red_count = 0
        self.black_count = 0
        self.red_king_count = 0
        self.black_king_count = 0
        self.store_piece_locations()

    def remove_piece(self, piece, remove_from_list=False):
        """
        Remove a piece from the board

        Args:
            piece, Piece: The piece to remove
            remove_from_list, bool: Whether to remove the piece from the game
        """
        # Get the location of the piece
        piece_location = piece.get_location()

        # Remove the piece from the board
        self.board[piece_location[0]][piece_location[1]] = None

        # Remove the piece from the list of pieces
        if remove_from_list:
            try: self.pieces.remove(piece) # Remove the piece from the list of pieces
            except ValueError:
                print ("Piece not found in list of pieces")
                print ("Piece: ", piece)
                print ("Piece List: ")
                self.print_pieces()
                quit()

    def add_piece(self, piece):
        """
        Add a piece to the board

        Args:
            piece, Piece: The piece to add

        Returns:
            bool: Whether the piece was added successfully
        """
        # Get the location of the piece
        piece_location = piece.get_location()

        #if there is already a piece at the location, return False
        if self.get_piece(piece_location[0], piece_location[1]) is not None:
            return False

        # Add the piece to the board
        self.board[piece_location[0]][piece_location[1]] = piece

        # Add the piece to the list of pieces
        self.pieces.append(piece)

        #update piece color counts
        if piece.color == 'red':
            self.red_count += 1
        else:
            self.black_count += 1
        # print("Restored: ", piece)
        return True

    def get_piece(self, row, col) -> Piece | None:
        """
        Get the piece at a given location

        Args:
            row, int: The row of the piece
            col, int: The column of the piece

        Returns:
            piece, Piece: The piece at the given location
        """
        return self.board[row][col]
    
    def print_pieces(self):
        """
        Print the pieces on the board
        """
        for piece in self.pieces:
            #print each piece string without a newline
            print(piece, end=" ")
        print()

    def clone(self) -> 'Board':
        """
        Create a deep copy of the board

        Returns:
            board, Board: A deep copy of the board
        """
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        new_board.pieces = [p.clone() for p in self.pieces]
        new_board.red_count = self.red_count
        new_board.black_count = self.black_count
        new_board.store_piece_locations()
        # print("Finished cloning??")
        return new_board

if __name__ == "__main__":
    layout = ['RE2', 'BD3K', 'BB5', 'BB7', 'BD7', 'BF5']
    game_board = Board(mode='custom', custom_layout=layout)
    game_board.draw_board()  # Display the board
    game_board.store_piece_locations()
    game_board.print_pieces()