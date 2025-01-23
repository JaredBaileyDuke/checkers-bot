from pymycobot.mycobot import MyCobot
from src.arm_actions.send_checkers_coords import *

def perform_robot_move(mc, robot_move):
    speed = 25
 
    move_list = create_move_list(robot_move)

    for move in move_list:
        checker_space_1 = move[0:2]
        checker_space_2 = move[3:]
        
        jump = False
        if abs(int(checker_space_1[1]) - int(checker_space_2[1])) == 2:
            jump = True

        # move 1
        # top numbers (8's)
        if checker_space_1[0].lower() in "abcdefgh" and int(checker_space_1[1]) == 8:
            angle_move(mc, checker_space_1, sleep_time=3, magnet="on")
            sleep(3)
        
        # numbers 1-7
        elif checker_space_1[0].lower() in "abcdefgh" and int(checker_space_1[1]) in range(1,8):
            coord_move(mc, checker_space_1, sleep_time=3, magnet="on")
            sleep(3)

        # move 2
        # top numbers (8's)
        if checker_space_2[0].lower() in "abcdefgh" and int(checker_space_2[1]) == 8:
            angle_move(mc, checker_space_2, sleep_time=3, magnet="off")
            sleep(3)
        
        # numbers 1-7
        elif checker_space_2[0].lower() in "abcdefgh" and int(checker_space_2[1]) in range(1,8):
            coord_move(mc, checker_space_2, sleep_time=3, magnet="off")
            sleep(3)

        # jump condition
        if jump == True:
            first = "A"
            second = "1"

            # print(checker_space_1[0].lower())
            # print(checker_space_2[0].lower())

            # find space jumped
            if checker_space_1[0].lower() in "ac" and checker_space_2[0].lower() in "ac":
                first = "B"
            elif checker_space_1[0].lower() in "bd" and checker_space_2[0].lower() in "bd":
                first = "C"
            elif checker_space_1[0].lower() in "ce" and checker_space_2[0].lower() in "ce":
                first = "D"
            elif checker_space_1[0].lower() in "df" and checker_space_2[0].lower() in "df":
                first = "E"
            elif checker_space_1[0].lower() in "eg" and checker_space_2[0].lower() in "eg":
                first = "F"
            elif checker_space_1[0].lower() in "fh" and checker_space_2[0].lower() in "fh":
                first = "G"
            if checker_space_1[1] in "13" and checker_space_2[1] in "13":
                second = "2"
            elif checker_space_1[1] in "24" and checker_space_2[1] in "24":
                second = "3"
            elif checker_space_1[1] in "35" and checker_space_2[1] in "35":
                second = "4"
            elif checker_space_1[1] in "46" and checker_space_2[1] in "46":
                second = "5"
            elif checker_space_1[1] in "57" and checker_space_2[1] in "57":
                second = "6"
            elif checker_space_1[1] in "68" and checker_space_2[1] in "68":
                second = "7"
            jump_move = first + second
            print(jump_move)

            # jump movement
            coord_move(mc, jump_move, sleep_time=3, magnet="on")
            sleep(3)
            coord_move(mc, "L1", sleep_time=3, magnet="off")
            sleep(3)



def create_move_list(robot_move):
    # separate moves into a list
    robot_move_list = robot_move.split(',')

    # remove leading spaces
    for item in robot_move_list:
        if item[0] == " ":
            item = item[1:]
    
    return robot_move_list


