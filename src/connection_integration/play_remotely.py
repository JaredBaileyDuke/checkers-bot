import sys
sys.path.append('..')
import socket
import robot_client as rc
from checkers_game.game import Game
from time import sleep

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
            print(message)

            #if the robot is playing, wait for 5 seconds (comment this out if user is playing)
            user = True
            if socket and not user: 
                # Send the message to the server
                client_socket.send(message.encode('utf-8'))
                # Wait for the robot to finish its turn
                sleep(5)
        else:
            # message = game.ai_turn(difficulty="Random")
            # message = game.ai_turn(difficulty="Prefer Jumps")
            # message = game.ai_turn(difficulty="LLM")
            message = game.ai_turn(difficulty="Minimax", minimax_depth=3)
            # game.user_turn()
            print(message)

            #if the robot is playing, wait for 5 seconds
            user = True
            if socket and not user: 
                # Send the message to the server
                client_socket.send(message.encode('utf-8'))
                # Wait for the robot to finish its turn
                sleep(5)

        if game.check_winner():
            message = "exit"
            print("Game over!")
            if socket: client_socket.send(message.encode('utf-8'))
            return message

        game.switch_turn()

        #see if user wants to exit
        # exit_message = input("Do you want to continue? (y/n): ")
        exit_message = "y"
        if exit_message == "n":
            message = "exit"
            if socket: client_socket.send(message.encode('utf-8'))
            return message

if __name__ == "__main__":
    # client_socket = rc.connect_to_robot()
    client_socket = None #for testing only (if you don't have a robot to connect to)
    #start the game
    game = Game()

    if play_with_robot(game, client_socket) == "exit":
        print("Exiting game")
        if client_socket: client_socket.close()
