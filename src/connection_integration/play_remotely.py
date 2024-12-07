import sys
sys.path.append('..')
import robot_client as rc
from checkers_game.game import Game
from time import sleep

def adapt_to_robot(message):
    '''
    Adapt the message to the robot's format, add jumps
    '''
    # Adapt the message to the robot's format
    message = message.lower()

    # Add jumps
    message_squares = message.split(" ")
    #find the locations the robot jumps over
    jumps = []
    for i in range(len(message_squares)):
        if i > 0:
            current_row = int(message_squares[i][1])
            current_col = ord(message_squares[i][0])
            destination_row = int(message_squares[i-1][1])
            destination_col = ord(message_squares[i-1][0])
            #if the absolute value of the difference between the two squares is 2, then there was a jump
            if abs(current_row - destination_row) == 2:
                jumpped_square = chr((current_col + destination_col) // 2) + str((current_row + destination_row) // 2)
                jumps.append(jumpped_square)
    
    print("Jumps: ", jumps)
    if len(jumps) > 0:
        message_moves = message.split(",")
        for i in range(len(jumps)):
            message_moves[i] = message_moves[i] + " J" + jumps[i]
        message = ",".join(message_moves)
    
    # if "," in message:
    #     print("Robot message: ", message)
    #     exit()

    return message

def play_with_robot(game, socket):
    """
    Game loop for robot play
    """
    message = ""
    while True:
        if game.turn == 'red':
            # message = game.ai_turn(difficulty="Random")
            # message = game.ai_turn(difficulty="Prefer Jumps")
            # message = game.ai_turn(difficulty="LLM")
            message = game.ai_turn(difficulty="Minimax", minimax_depth=3)
            # self.user_turn()

            #if the robot is playing, wait for 5 seconds (comment this out if user is playing)
            user = False
            if not user:
                message = adapt_to_robot(message)
                print(message)
                if socket: 
                    # Send the message to the server
                    client_socket.send(message.encode('utf-8'))
                    # Wait for the robot to finish its turn
                    #wait for a "complete" message from the robot
                    recieve_message = rc.receive_message(client_socket)
                    while recieve_message != "complete":
                        recieve_message = rc.receive_message(client_socket)
                        print("Waiting for robot to finish...")
        else:
            # message = game.ai_turn(difficulty="Random")
            message = game.ai_turn(difficulty="Prefer Jumps")
            # message = game.ai_turn(difficulty="LLM")
            # message = game.ai_turn(difficulty="Minimax", minimax_depth=3)
            # user_input = input("Enter your move (e.g., 'a3 b4'): ")
            # if user_input == "exit":
            #     return "exit"
            # game.user_turn(user_input)

            #if the robot is playing, wait for 5 seconds (comment this out if user is playing)
            user = False
            if not user:
                message = adapt_to_robot(message)
                print(message)
                if socket: 
                    # Send the message to the server
                    client_socket.send(message.encode('utf-8'))
                    # Wait for the robot to finish its turn
                    #wait for a "complete" message from the robot
                    recieve_message = rc.receive_message(client_socket)
                    while recieve_message != "complete":
                        recieve_message = rc.receive_message(client_socket)
                        print("Waiting for robot to finish...")

        if game.check_winner():
            message = "exit"
            print("Game over!")
            if socket: client_socket.send(message.encode('utf-8'))
            return message

        game.switch_turn()
        game.board.draw_board()

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
    client_socket = rc.connect_to_robot()
    # client_socket = None #for testing only (if you don't have a robot to connect to)
    #start the game
    game = Game()
    game.board.draw_board()

    if play_with_robot(game, client_socket) == "exit":
        if client_socket: client_socket.send("exit".encode('utf-8'))
        print("Exiting game")
        if client_socket: client_socket.close()
