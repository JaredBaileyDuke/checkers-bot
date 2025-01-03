class Piece:
    def __init__(self, color, location, king=False):
        """
        Initialize a piece with a specific color

        Args:
            color, string: The color of the piece (e.g., 'red' or 'black')
            location, tuple: The current location of the piece on the board
                - row: The row of the board (0-7)
                - col: The column of the board (0-7)
        
        Attributes:
            color: The color of the piece
            king: A boolean indicating if the piece is a king
        """
        self.color = color  # Color of the piece
        self.location = location  # Current location of the piece
        self.king = False  # Indicates if the piece is a king
        self.crowned = False  # Indicates if the piece has been crowned by the robot
        self.move_directions = []  # List of potential move directions
        self.jump_directions = []
        self.extra_jump = False
        self.potential_move_directions(self.location) # Initialize potential move directions
        self.potential_jump_directions(self.location) # Initialize potential jump directions

    def promote_to_king(self):
        """
        Promote the piece to a king
        """
        # print(f"Piece at {self.get_location()} promoted to king!")
        self.king = True

        # Update potential move and jump directions
        self.potential_move_directions(self.location)
        self.potential_jump_directions(self.location)

    def demote_from_king(self, print_message=False):
        """
        Demote the piece from a king
        """
        if print_message:
            print(f"Piece at {self.get_location()} demoted from king!")
        self.king = False

        # Update potential move and jump directions
        self.potential_move_directions(self.location)
        self.potential_jump_directions(self.location)

    def move(self, dest_row, dest_col):
        """
        Move the piece to a new location

        Args:
            dest_row: The row of the destination location
            dest_col: The column of the destination location
        """
        # Update the location of the piece
        self.location: tuple[int,int] = (dest_row, dest_col)

        # Update potential move and jump directions
        self.potential_move_directions(self.location)
        self.potential_jump_directions(self.location)

    def potential_move_directions(self, curr_location):
        """
        Store potential move directions based on the current location of the piece

        This method does not account for other pieces on the board

        Args:
            curr_location: The destination location of the piece on the board (row, col)
        """
        # Reset directions based on current location
        row, col = curr_location
        
        # Determine potential move directions based on king status
        if self.king:
            self.move_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if self.color == 'black':
                self.move_directions = [(-1, -1), (-1, 1)] 
            else:
                self.move_directions = [(1, -1), (1, 1)]

        # Check for edges of the board, remove options that go off the board
        if row == 0: # Top row
            if self.move_directions.__contains__((-1, -1)):
                self.move_directions.remove((-1, -1))
            if self.move_directions.__contains__((-1, 1)):
                self.move_directions.remove((-1, 1))
        elif row == 7: # Bottom row
            if self.move_directions.__contains__((1, -1)):
                self.move_directions.remove((1, -1))
            if self.move_directions.__contains__((1, 1)):
                self.move_directions.remove((1, 1))
        if col == 0: # Left column
            if self.move_directions.__contains__((-1, -1)):
                self.move_directions.remove((-1, -1))
            if self.move_directions.__contains__((1, -1)):
                self.move_directions.remove((1, -1))
        elif col == 7: # Right column
            if self.move_directions.__contains__((-1, 1)):
                self.move_directions.remove((-1, 1))
            if self.move_directions.__contains__((1, 1)):
                self.move_directions.remove((1, 1))

    def potential_jump_directions(self, curr_location):
        """
        Store potential jump directions based on the current location of the piece

        This method does not account for other pieces on the board

        Args:
            curr_location: The destination location of the piece on the board (row, col)
        """
        # Reset directions based on current location
        row, col = curr_location

        # Determine potential jump directions based on king status
        if self.king:
            self.jump_directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        else:
            if self.color == 'black':
                self.jump_directions = [(-2, -2), (-2, 2)]
            else:
                self.jump_directions = [(2, -2), (2, 2)]

        # Check for edges of the board, remove options that go off the board
        if row <= 1: # Top rows
            if self.jump_directions.__contains__((-2, -2)):
                self.jump_directions.remove((-2, -2))
            if self.jump_directions.__contains__((-2, 2)):
                self.jump_directions.remove((-2, 2))
        elif row >= 6: # Bottom rows
            if self.jump_directions.__contains__((2, -2)):
                self.jump_directions.remove((2, -2))
            if self.jump_directions.__contains__((2, 2)):
                self.jump_directions.remove((2, 2))
        if col <= 1: # Left columns
            if self.jump_directions.__contains__((-2, -2)):
                self.jump_directions.remove((-2, -2))
            if self.jump_directions.__contains__((2, -2)):
                self.jump_directions.remove((2, -2))
        elif col >= 6: # Right columns
            if self.jump_directions.__contains__((-2, 2)):
                self.jump_directions.remove((-2, 2))
            if self.jump_directions.__contains__((2, 2)):
                self.jump_directions.remove((2, 2))

    def get_location(self):
        """
        Return the current location of the piece
        """
        return self.location
    
    def get_color(self):
        """
        Return the color of the piece
        """
        return self.color
    
    def get_king(self):
        """
        Return the king status of the piece
        """
        return self.king
    
    def get_crowned(self):
        """
        Return the crowned status of the piece
        """
        return self.crowned
    
    def crown(self):
        """
        Crown the piece
        """
        self.crowned = True
    
    def get_potential_move_directions(self):
        """
        Return the potential move directions of the piece
        """
        return self.move_directions
    
    def get_potential_jump_directions(self):
        """
        Return the potential jump directions of the piece
        """
        return self.jump_directions

    def clone(self):
        """
        Return a copy of the piece
        """
        return Piece(self.color, self.location, self.king)

    def __str__(self):
        """
        Return a string representation of the piece
        """
        return f"{self.color[0].upper()}{self.location}{'K' if self.king else ''}"
    
    def __eq__(self, other):
        return self.color == other.color and self.location == other.location
    

if __name__ == "__main__":
    # Example usage
    red_piece = Piece('red', (2, 3))
    print(red_piece)  # Output: R(2, 3)
    red_piece.promote_to_king()
    print(red_piece)  # Output: R(2, 3)K
    red_piece.move(3, 4)
    print(red_piece)  # Output: R(3, 4)K