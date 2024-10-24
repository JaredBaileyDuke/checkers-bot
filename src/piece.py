class Piece:
    def __init__(self, color, location):
        """
        Initialize a piece with a specific color
        Args:
            color: The color of the piece (e.g., 'Red' or 'Black')
            location: The current location of the piece on the board (0-32)
                - 0 for not on the board
                - 1-32 for positions on the board
        Attributes:
            color: The color of the piece
            king: A boolean indicating if the piece is a king
        """
        self.color = color  # Color of the piece
        self.location = location  # Current location of the piece
        self.king = False  # Indicates if the piece is a king

    def promote_to_king(self):
        """
        Promote the piece to a king
        """
        self.king = True

    def move(self, new_location):
        """
        Move the piece to a new location
        Args:
            new_location: The new location of the piece on the board (0-32)
        """
        self.location = new_location

    def __str__(self):
        """
        Return a string representation of the piece
        """
        return f"{self.color[0].upper()}{self.location}{'K' if self.king else ''}"
    

