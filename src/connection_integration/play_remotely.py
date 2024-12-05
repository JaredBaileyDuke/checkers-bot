import socket
import robot_client as rc
from ..checkers_game import Game
from time import sleep

def play_with_robot(game):
    """
    Game loop for robot play
    """
    message = ""
    while True:
        if game.turn == 'red':
            message = game.ai_turn(difficulty="Random")
            # print(self.ai_turn(difficulty="Prefer Jumps"))
            # print(self.ai_turn(difficulty="LLM"))
            # print(self.ai_turn(difficulty="Minimax"))
            # self.user_turn()
        else:
            # message = game.ai_turn(difficulty="Random")
            # print(self.ai_turn(difficulty="Prefer Jumps"))
            # print(self.ai_turn(difficulty="LLM"))
            # print(self.ai_turn(difficulty="Minimax"))
            game.user_turn()

        if game.check_winner():
            message = "exit"
            client_socket.send(message.encode('utf-8'))
            return message

        game.switch_turn()
        # self.board.print_pieces()
        # Send the message to the server
        print(message)
        client_socket.send(message.encode('utf-8'))

        #see if user wants to exit
        message = input("Do you want to exit? (y/n): ")
        if message == "y":
            message = "exit"
            client_socket.send(message.encode('utf-8'))
            return message

        sleep(5)

if __name__ == "__main__":
    client_socket = rc.connect_to_robot()
    #start the game
    game = Game()

    if play_with_robot(game) == "exit":
        print("Exiting game")
        client_socket.close()
