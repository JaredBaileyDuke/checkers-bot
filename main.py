from pymycobot.mycobot import MyCobot
from src.checkers_game.game import Game
from time import sleep

if __name__ == '__main__':
    mc = MyCobot("/dev/ttyAMA0", 1000000) # startup robot
    speed = 25 # set speed
    starting_angles = [0, -40, -20, 0, 0, 0]  # starting location, up in air
    mc.send_angles(starting_angles, speed)
    sleep(1)

    game = Game()
    game.play(mc)