from .board import Board, Piece
import random
from time import sleep
import openai
import os

class Game:
    def __init__(self):
        """
        Set up the game
        """
        self.board = Board()
        self.turn = 'red'  # Starting player
        self.opponent = 'black'
        self.valid_moves = {}
        self.tie = False

    def switch_turn(self):
        """
        Switch the turn to the other player
        """
        if self.turn == 'red':
            self.turn = 'black'
            self.opponent = 'red'
        else:
            self.turn = 'red'
            self.opponent = 'black'

    def user_turn(self, move = None, show_board=False, restricted_jump=None):
        """
        User turn logic

        Args:
            move, str: The move in the format 'A3 B4'
            show_board, bool: Whether to show the board
            restricted_jump, tuple: piece location - since a jump occurred, the user must continue jumping with the same piece
        """
        if show_board: self.board.draw_board()
        print(f"{self.turn.capitalize()}'s turn")

        #Get and parse user input
        while True:
            # Get user input for piece selection and move
            if move is None:
                user_input = input("Enter your move (e.g., 'A3 B4'): ")
            else:
                user_input = move

            try:
                start, end = user_input.split()
                start_row, start_col = int(start[1]) - 1, ord(start[0].upper()) - ord('A')
                dest_row, dest_col = int(end[1]) - 1, ord(end[0].upper()) - ord('A')  
            except (ValueError, IndexError):
                move = None
                print("Invalid input. Please enter in the format 'A3 B4'.")
                continue

            #if a jump is restricted, make sure the user jumps with that piece
            if restricted_jump is not None:
                if (start_row, start_col) != restricted_jump:
                    move = None
                    print("You must jump with the piece at", chr(restricted_jump[1] + ord('A')) + str(restricted_jump[0] + 1))
                    continue

            #Make sure piece exists in the start location
            if self.board.get_piece(start_row, start_col) is None:
                move = None
                print("No piece at that location!")
                continue

            #Make sure piece is the correct color
            if self.board.get_piece(start_row, start_col).color != self.turn:
                move = None
                print("Wrong color piece! It's " + self.turn + "'s turn.")
                print("You are trying to move a " + self.board.get_piece(start_row, start_col).color + " piece.")
                continue

            #Make sure move is valid
            valid_moves = self.board.find_valid_moves_and_jumps(self.board.get_piece(start_row, start_col), restricted_jump is not None)
            if (dest_row, dest_col) not in valid_moves:
                move = None
                print("Invalid move for piece", self.board.get_piece(start_row, start_col))
                print("Valid moves are: " + str(valid_moves))
                continue

            break

        # Get the piece to move
        piece = self.board.get_piece(start_row, start_col)

        # Move the piece
        self.board.move_piece(piece, dest_row, dest_col)
        print("Moved " + piece.color + " piece from " + start + " to " + end)

        if piece.extra_jump:
            print("Extra jump available!")
            self.user_turn(restricted_jump=(dest_row, dest_col))

    def ai_turn(self, difficulty="Random", show_board = False, restricted_jump=None, minimax_depth=3):
        """
        AI turn logic with difficulty setting
        - Random: Choose a random move

        Args:
            restricted_jump, tuple: since a jump occurred, the AI must continue jumping with the same piece

        Returns:
            str: The move in the format 'A3 B4'
        """
        # Show the board and print the current player's turn
        if show_board: self.board.draw_board()
        print(f"{self.turn.capitalize()}'s turn")

        # Get the best move for the AI
        if difficulty == "Random":
            move = self.make_random_move()
        elif difficulty == "Minimax":
            move = self.make_minimax_move(depth = minimax_depth)
        elif difficulty == "Prefer Jumps":
            move = self.make_prefer_jumps()
        elif difficulty == "LLM":
            move = self.make_llm_move()
        
        return move

    def make_minimax_move(self, restricted_jump=None, depth=3):
        """
        Make a move for the AI using the minimax algorithm

        Args:
            restricted_jump, tuple: location - since a jump occurred, the AI must continue jumping with the same piece
        """
        # If no restricted jump, do a minimax search
        if restricted_jump is None: 
            score, result = self.minimax(depth, True, self.board)
            if result is None:
                self.tie = True
                return "No moves available"
            piece, dest = result

        # If a restricted jump, choose the piece that must jump
        else: 
            temp_piece: Piece = self.board.get_piece(restricted_jump[0], restricted_jump[1]) # Get the piece that must jump
            valid_moves = self.board.find_valid_moves_and_jumps(temp_piece, only_jumps=True) # Get all valid jumps for the piece
            piece, dest =  temp_piece, valid_moves[0]

        # Get piece location, and destination location
        start_row, start_col = piece.get_location()
        dest_row, dest_col = dest
        
        # Move the piece
        self.board.move_piece(piece, dest_row, dest_col)
        print("Moved " + piece.color + " piece from " + chr(start_col + ord('A')) + str(start_row + 1) + " to " + chr(dest_col + ord('A')) + str(dest_row + 1))

        #Get move in a string (e.g., 'A3 B4')
        move = chr(start_col + ord('A')) + str(start_row + 1) + " " + chr(dest_col + ord('A')) + str(dest_row + 1)

        # Check if the piece can make an extra jump
        if piece.extra_jump:
            print("Extra jump available!")
            previous_move = move
            move = self.make_minimax_move(restricted_jump=(dest_row, dest_col))
            move = previous_move + ", " + move

        return move
            
    def minimax(self, depth: int, maximizing_player: bool, board: Board) -> tuple[float, tuple[Piece, tuple[int, int]]]:
        """
        Minimax algorithm to find the best move for the AI

        Args:
            depth, int: The depth of the search tree
            maximizing_player, bool: Whether the AI is the maximizing player

        Returns:
            float: The evaluation score
            tuple[Piece, tuple[int, int]: the piece to move and its associated move
        """
        # Base case
        if depth == 0 or self.check_winner(show_board=False):
            return self.evaluate(board), None
        
        best_move: None | tuple[Piece, float, tuple[int, int]] = None
        if maximizing_player:
            max_eval = float('-inf')
        else:
            max_eval = float('inf')

        for piece in board.find_color_pieces(self.turn):
            for move in board.find_valid_moves_and_jumps(piece):
                dest =  move
                # Get piece location, and destination location
                dest_row, dest_col = dest
                # Move the piece
                board_copy = board.clone()
                board_copy.move_piece(piece, dest_row, dest_col)
                eval = self.minimax(depth - 1, False, board_copy)[0]
                if maximizing_player:
                    if eval > max_eval:
                        best_move = (piece, move)
                    max_eval = max(max_eval, eval)
                else:
                    if eval < max_eval:
                        best_move = (piece, move)
                    max_eval = min(max_eval, eval)

        return max_eval, best_move

    def evaluate(self, board):
        """
        Evaluate the board state for the AI

        Returns:
            int: The evaluation score
        """
        #count the number of pieces for each color
        red_pieces = board.red_count
        black_pieces = board.black_count

        red_kings = board.red_king_count
        black_kings = board.black_king_count

        #return the difference in the number of pieces
        if self.turn == 'red':
            score = (red_pieces - black_pieces) - black_kings + red_kings*5
            return score
        else:
            score = (black_pieces - red_pieces) - red_kings + black_kings*5
            return score

    def make_llm_move(self):
        """
        Make a move by calling a LLM model

        Args:
            restricted_jump, tuple: location - since a jump occurred, the AI must continue jumping with the same piece

        Returns:
            str: The move in the format 'A3 B4'
        """
        prompt = f"\
            Choose the next move as {self.turn}. It must be in the form of: piece number, \
                destination row, destination column \n\
            For example: 3,0,7 \n\n\
            Use the following board information to make your decision: \n\
            "
        
        for color in ["red", "black"]:
            i = 0
            for piece in self.board.find_color_pieces(color):
                prompt += f"Piece {i}: \n\
                Color: {piece.get_color()} \n\
                Location: {piece.get_location()} \n\
                King: {piece.get_king()} \n\
                Valid Moves: {self.board.find_valid_moves_and_jumps(piece, only_jumps=False)} \n\n\
                "   
                i += 1


        prompt += "Rememeber to use the format of 5, 7, 0. Your move: "

        try:
            # read in api key from file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, ".apis", "CHATGPT.txt")
            with open(file_path, 'r') as f:
                api_key = f.read().strip()

            # call the LLM model to get the next move
            response = self.call_openai_api(prompt, api_key)
            print("LLM Response: ", response)

            # Parse the response to get the move
            piece_num, dest_row, dest_col = response.split(',')
            print(piece_num, dest_row, dest_col)
            piece = self.board.find_color_pieces(self.turn)[int(piece_num)]
            dest_row, dest_col = int(dest_row), int(dest_col)

            # Get piece location
            start_row, start_col = piece.get_location()

            # prints
            print(f"Color: {piece.get_color()} \n\
                Location: {piece.get_location()} \n\
                King: {piece.get_king()} \n\n")
            print(f"Destination: {dest_row}, {dest_col}")

            # Move the piece               
            self.board.move_piece(piece, dest_row, dest_col)
            print("LLM Moved " + piece.color)

            #Get move in a string (e.g., 'A3 B4')
            move = chr(start_col + ord('A')) + str(start_row + 1) + " " + chr(dest_col + ord('A')) + str(dest_row + 1)

        except:
            print("Error making move with LLM")
            move = self.make_prefer_jumps()

        # Check if the piece can make an extra jump
        if piece.extra_jump:
            print("Extra jump available!")
            previous_move = move
            move = self.make_prefer_jumps(restricted_jump=(dest_row, dest_col))
            move = previous_move + ", " + move

        return move
            
    def call_openai_api(self, prompt, key):
        """
        Call the OpenAI API to get the next move

        Args:
            prompt, str: The prompt to send to the API
            key, str: The API key

        Returns:
            str: The response from the API
        """
        
        openai.api_key = key

        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': "You are an AI playing checkers. You must carefully and accurately choose your next move. Rememeber to use the format: 5, 7, 0."},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )

        return response.choices[0].message['content'].strip()

    def make_prefer_jumps(self, restricted_jump=None):
        """
        Make a move for the AI that prefers jumps

        Args:
            restricted_jump, tuple: location - since a jump occurred, the AI must continue jumping with the same piece
        
        Returns:
            str: The move in the format 'A3 B4'
        """
        # If no restricted jump, choose a random piece
        if restricted_jump is None: 
            # Get all pieces of the given color
            valid_pieces = self.board.find_color_pieces(self.turn)
            valid_moves = []

            # Look through pieces to find one that can jump, choose the first piece that can jump
            for p in valid_pieces:
                piece = p
                valid_moves = self.board.find_valid_moves_and_jumps(p, only_jumps=True)
                if len(valid_moves) > 0:
                    dest = valid_moves[0]
                    break
            
            # If no jumps, make a random move
            if len(valid_moves) == 0:
                move = self.make_random_move()
                return move
        
        # If a restricted jump, choose the piece that must jump
        else:
            temp_piece = self.board.get_piece(restricted_jump[0], restricted_jump[1]) # Get the piece that must jump
            valid_moves = self.board.find_valid_moves_and_jumps(temp_piece, only_jumps=True) # Get all valid jumps for the piece
            piece, dest = temp_piece, valid_moves[0]

        # Get piece location, and destination location
        start_row, start_col = piece.get_location()
        dest_row, dest_col = dest

        # Move the piece
        self.board.move_piece(piece, dest_row, dest_col)
        print("Moved " + piece.color + " piece from " + chr(start_col + ord('A')) + str(start_row + 1) + " to " + chr(dest_col + ord('A')) + str(dest_row + 1))

        #Get move in a string (e.g., 'A3 B4')
        move = chr(start_col + ord('A')) + str(start_row + 1) + " " + chr(dest_col + ord('A')) + str(dest_row + 1)

        # Check if the piece can make an extra jump
        if piece.extra_jump:
            print("Extra jump available!")
            previous_move = move
            move = self.make_prefer_jumps(restricted_jump=(dest_row, dest_col))
            move = previous_move + ", " + move

        return move
            
    def make_random_move(self, restricted_jump=None):
        """
        Make a random move for the AI

        Args:
            restricted_jump, tuple: location - since a jump occurred, the AI must continue jumping with the same piece

        Returns:
            str: The move in the format 'A3 B4'
        """
        # If no restricted jump, choose a random piece
        if restricted_jump is None: 
            valid_moves = self.find_valid_moves(self.turn)
            if len(valid_moves) == 0:
                self.tie = True
                return "No moves available"
            #shuffle the list of valid moves
            random.shuffle(valid_moves)
            piece, dest = valid_moves[0]
            # print(piece, dest)

        # If a restricted jump, choose the piece that must jump
        else: 
            temp_piece = self.board.get_piece(restricted_jump[0], restricted_jump[1]) # Get the piece that must jump
            valid_moves = self.board.find_valid_moves_and_jumps(temp_piece, only_jumps=True) # Get all valid jumps for the piece
            piece, dest =  temp_piece, valid_moves[0]

        # Get piece location, and destination location
        start_row, start_col = piece.get_location()
        dest_row, dest_col = dest

        # Move the piece
        self.board.move_piece(piece, dest_row, dest_col)
        print("Moved " + piece.color + " piece from " + chr(start_col + ord('A')) + str(start_row + 1) + " to " + chr(dest_col + ord('A')) + str(dest_row + 1))

        #Get move in a string (e.g., 'A3 B4')
        move = chr(start_col + ord('A')) + str(start_row + 1) + " " + chr(dest_col + ord('A')) + str(dest_row + 1)

        # Check if the piece can make an extra jump
        if piece.extra_jump:
            print("Extra jump available!")
            previous_move = move
            move = self.make_random_move(restricted_jump=(dest_row, dest_col))
            move = previous_move + ", " + move

        return move
    
    def find_valid_moves(self, color):
        """
        Find all valid moves for a given color

        Args:
            color, str: The color of the pieces

        Returns:
            list: The list of valid moves for the given color
        """
        pieces: list[Piece] = self.board.find_color_pieces(color)
        valid_moves: list[list[tuple[int,int]]] = []
        for piece in pieces:
            for move in self.board.find_valid_moves_and_jumps(piece):
                valid_moves.append((piece, move))

        return valid_moves

    def check_winner(self, show_board=True):
        """
        Check if the game is over and print the winner

        Args:
            show_board, bool: Whether to show the board and print the winner

        Returns:
            bool: True if the game is over, False otherwise
        """

        red_pieces = self.board.red_count
        black_pieces = self.board.black_count
    
        if red_pieces == 0:
            if show_board: 
                self.board.draw_board()
                print("Black wins!")
            return True
        elif black_pieces == 0:
            if show_board:
                self.board.draw_board()
                print("Red wins!")
            return True
        elif self.tie:
            if show_board:
                self.board.draw_board()
                print("It's a tie!")
            return True
        return False
    
    def play(self):
        """
        Game loop
        """
        while True:
            if self.turn == 'red':
                print(self.ai_turn(difficulty="Random"))
                # print(self.ai_turn(difficulty="Prefer Jumps"))
                # print(self.ai_turn(difficulty="LLM"))
                # print(self.ai_turn(difficulty="Minimax"))
                # self.user_turn()
            else:
                print(self.ai_turn(difficulty="Random"))
                # print(self.ai_turn(difficulty="Prefer Jumps"))
                # print(self.ai_turn(difficulty="LLM"))
                # print(self.ai_turn(difficulty="Minimax"))
                # self.user_turn()
            if self.check_winner():
                break
            self.switch_turn()
            # self.board.print_pieces()
            self.board.draw_board()
            sleep(0.5)

if __name__ == "__main__":
    game = Game()
    game.play()