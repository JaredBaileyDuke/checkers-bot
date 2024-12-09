import sys
sys.path.append('..')
import robot_client as rc
from checkers_game.game import Game
from voice_clone import voice_clone
from time import sleep
import pygame
from cv import take_photo as tp
import cv2

def adapt_to_robot(message, game):
    '''
    Adapt the message to the robot's format, add jumps
    '''
    # Adapt the message to the robot's format
    message = message.lower()

    # Add jumps
    message_squares = message.split(" ")
    #find the locations the robot jumps over
    jumps = []
    kings = []
    i = 1
    #find the end location of the piece
    end_row, end_col = (int(message_squares[-1][1])-1), (ord(message_squares[-1][0])-97)
    while i < len(message_squares):
        if i > 0:
            current_row = int(message_squares[i-1][1])
            current_col = ord(message_squares[i-1][0])
            destination_row = int(message_squares[i][1])
            destination_col = ord(message_squares[i][0])
            #if the absolute value of the difference between the two squares is 2, then there was a jump
            if abs(current_row - destination_row) == 2:
                jumpped_square = chr((current_col + destination_col) // 2) + str((current_row + destination_row) // 2)
                jumps.append(jumpped_square)
            #if the destination square is on the last row, then the piece is a king
            if destination_row == 8 or destination_row == 1:
                #see if the piece is already a king
                if game.board.get_piece(end_row,end_col).get_crowned() == False:
                    kings.append(message_squares[i][0:2])
                    #crown the piece
                    game.board.get_piece(end_row,end_col).crown()
        i += 2
    
    print("Jumps: ", jumps)
    if len(jumps) > 0 or len(kings) > 0:
        message_moves = message.split(",")
        #search the message for the moves that need to be kinged
        for i in range(len(message_moves)):
            for king in kings:
                if (message_moves[i][-2:].lower()) == str(king).lower():
                    message_moves[i] = message_moves[i] + "K"

        #add the jumps to the message
        for i in range(len(jumps)):
            message_moves[i] = message_moves[i] + " J" + jumps[i]
        message = ",".join(message_moves)

    return message

def robot_turn(game, message, socket, speaking = True, delay = 0):
    """
    Robot's turn
    """
    message = adapt_to_robot(message, game)
    print(message)
    #play the audio
    if speaking:
        print(voice_clone.play_premade_audio())
    if socket: 
        # Send the message to the server
        client_socket.send(message.encode('utf-8'))
        # Wait for the robot to finish its turn
        #wait for a "complete" message from the robot
        recieve_message = rc.receive_message(client_socket)
        while recieve_message != "complete":
            recieve_message = rc.receive_message(client_socket)
            print("Waiting for robot to finish...")
    #wait for the audio to finish playing
    while speaking and pygame.mixer.music.get_busy():
        pass

def play_with_robot(game, socket, cap, speaking = True, delay = 0):
    """
    Game loop for robot play
    """
    message = ""
    while True:
        if game.turn == 'red':
            # message = game.ai_turn(difficulty="Random")
            # message = game.ai_turn(difficulty="Prefer Jumps")
            # message = game.ai_turn(difficulty="LLM")
            # message = game.ai_turn(difficulty="Minimax", minimax_depth=3)

            #if the robot is playing
            user = True
            if not user:
                robot_turn(game, message, socket, speaking = speaking)
            else:
                #give the user 5 seconds to make a move
                print("You have 5 seconds to make a move")
                for i in range(5):
                    sleep(1)
                    print(5-i)
                # Capture the frame
                frame = tp.capture_frame(cap)
                piece_locations = tp.cv_process_image(frame)
                layout = tp.return_board_layout(piece_locations)
                game = Game(board_mode = mode, layout = layout, start_player = 'red')
        else:
            # message = game.ai_turn(difficulty="Random")
            message = game.ai_turn(difficulty="Prefer Jumps")
            # message = game.ai_turn(difficulty="LLM")
            # message = game.ai_turn(difficulty="Minimax", minimax_depth=3)
            # user_input = input("Enter your move (e.g., 'a3 b4'): ")
            # if user_input == "exit":
            #     return "exit"
            # game.user_turn(user_input)

            #if the robot is playing
            user = False
            if not user:
                robot_turn(game, message, socket, speaking = speaking)

        if game.check_winner():
            message = "exit"
            print("Game over!")
            if socket: client_socket.send(message.encode('utf-8'))
            return message

        game.switch_turn()
        game.board.draw_board()
        sleep(delay)

        #see if user wants to exit
        # exit_message = input("Do you want to continue? (y/n): ")
        exit_message = "y"
        if exit_message != "n":
            if exit_message == "away":
                message = "away"
                if socket: client_socket.send(message.encode('utf-8'))
            continue
        else:
            message = "exit"
            if socket: client_socket.send(message.encode('utf-8'))
            return message

if __name__ == "__main__":
    # client_socket = rc.connect_to_robot()
    client_socket = None #for testing only (if you don't have a robot to connect to)

    cap = tp.initialize_webcam()

    #start the game
    mode = 'custom' # 'classic' or 'custom'
    frame = tp.capture_frame(cap)
    piece_locations = tp.cv_process_image(frame)
    layout = tp.return_board_layout(piece_locations)
    game = Game(board_mode = mode, layout = layout)
    game.board.draw_board()

    try:
        if play_with_robot(game, client_socket, cap, speaking=False, delay=0.5) == "exit":
            if client_socket: client_socket.send("exit".encode('utf-8'))
            print("Exiting game")
            if client_socket: client_socket.close()

    #keyboard interrupt
    except KeyboardInterrupt:
        if client_socket: client_socket.send("exit".encode('utf-8'))
        print("Exiting game")
        if client_socket: client_socket.close()
        # Release the webcam and close any open windows
        if cap: 
            cap.release()
            cv2.destroyAllWindows()
