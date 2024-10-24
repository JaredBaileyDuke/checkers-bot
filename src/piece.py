class Piece:
    def __init__(self, color, location):
        """
        Initialize a piece with a specific color
        Args:
            color, string: The color of the piece (e.g., 'Red' or 'Black')
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
        self.directions = []  # List of potential move directions
        self.potential_move_directions(self.location) # Initialize potential move directions

    def promote_to_king(self):
        """
        Promote the piece to a king
        """
        self.king = True

    def move(self, dest_row, dest_col):
        """
        Move the piece to a new location
        Args:
            new_location: The new location of the piece on the board (0-32)
        """
        # Update the location of the piece
        self.location = (dest_row, dest_col)

        # Update potential move directions after moving the piece
        self.potential_move_directions(self.location)

    def jump(self, dest_row, dest_col):
        """
        Jump over an opponent's piece
        Args:
            dest_row: The row of the destination location
            dest_col: The column of the destination location
        """
        # Update the location of the piece
        self.location = (dest_row, dest_col)

        # Update potential jump directions after jumping
        self.potential_jump_directions(self.location)

    def potential_move_directions(self, dest_location):
        """
        Store potential move directions based on the current location of the piece

        Args:
            dest_location: The destination location of the piece on the board (row, col)
        """
        # Reset directions based on current location
        row, col = dest_location
        
        # Determine potential move directions based on king status
        if self.king:
            self.directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            [(-1, -1), (-1, 1)] if self._color == 'Red' else [(1, -1), (1, 1)]

        # Check for edges of the board, remove options that go off the board
        if row == 0: # Top row
            self.directions.remove((-1, -1))
            self.directions.remove((-1, 1))
        elif row == 7: # Bottom row
            self.directions.remove((1, -1))
            self.directions.remove((1, 1))
        if col == 0: # Left column
            self.directions.remove((-1, -1))
            self.directions.remove((1, -1))
        elif col == 7: # Right column
            self.directions.remove((-1, 1))
            self.directions.remove((1, 1))

    def potential_jump_directions(self, dest_location):
        """
        Store potential jump directions based on the current location of the piece

        Args:
            dest_location: The destination location of the piece on the board (row, col)
        """
        # Reset directions based on current location
        row, col = dest_location

        # Determine potential jump directions based on king status
        if self.king:
            self.directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        else:
            self.directions = [(-2, -2), (-2, 2)] if self.color == 'Red' else [(2, -2), (2, 2)]

        # Check for edges of the board, remove options that go off the board
        if row <= 1: # Top rows
            self.directions.remove((-2, -2))
            self.directions.remove((-2, 2))
        elif row >= 6: # Bottom rows
            self.directions.remove((2, -2))
            self.directions.remove((2, 2))
        if col <= 1: # Left columns
            self.directions.remove((-2, -2))
            self.directions.remove((2, -2))
        elif col >= 6: # Right columns
            self.directions.remove((-2, 2))
            self.directions.remove((2, 2))

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
    
    def get_king_status(self):
        """
        Return the king status of the piece
        """
        return self.king
    
    def get_directions(self):
        """
        Return the potential move directions of the piece
        """
        return self.directions

    def __str__(self):
        """
        Return a string representation of the piece
        """
        return f"{self.color[0].upper()}{self.location}{'K' if self.king else ''}"
    

