from pymycobot.mycobot import MyCobot
import sys
import os
from time import sleep
import electromagnet_gpio
sys.path.append(os.path.dirname(__file__))

def convert_to_angles(checker_space):
    """
    Give angles based on entered checker space
    For use with joint space

    Args:
        checker_space, str: Space on checkerboard (ex. a8)

    Returns:
        angles, list: List of angles (-180 to 180 for most joints)
    """
    angle_dict = {
        'a8': [-2, -64, -16, -10, 0, 0],
        'b8': [3, -62, -21, -7, 0, 0],
        'c8': [7, -59, -27, -5, 0, 0],
        'd8': [13, -52, -40, 2, 0, 0],
        'e8': [18, -52, -40, 2, 0, 0],
        'f8': [23, -59, -27, -5, 0, 0],
        'g8': [27, -62, -21, -7, 0, 0],
        'h8': [32, -64, -16, -10, 0, 0]
    }

    angles = angle_dict[checker_space.lower()] 

    return angles

def angle_space_before_after(angles):
    """
    Give before and after angles based on board level angles
    For use with joint space

    Args:
        angles, list: Joint space on checkerboard

    Returns:
        angles_ba list: List of angles just above checkerboard angles
    """
    angles_ba = angles.copy()
    angles_ba[1] += 10

    return angles_ba

def angle_move(mc, checker_space, sleep_time, magnet="off"):
    """
    Give movements based on entered checker space
    For use with operational space

    Args:
        mc, object: MyCobot object
        checker_space, str: Space on checkerboard (ex. a8)
        sleep_time, int: Rest time between robot movements
        magnet, str: Electromagnet relay setting

    Returns:
        None
    """
    # get coordinates
    angles = convert_to_angles(checker_space)
    angles_ba = angle_space_before_after(angles)

    #movements
    mc.send_angles(angles_ba, speed)
    sleep(sleep_time)
    mc.send_angles(angles, speed)
    sleep(sleep_time)
    electromagnet(relay=magnet)
    sleep(1)
    mc.send_angles(angles_ba, speed)
    sleep(sleep_time)

def convert_to_coords(checker_space):
    """
    Give coordinates based on entered checker space
    For use with operational space

    Args:
        checker_space, str: Space on checkerboard (ex. a7)

    Returns:
        checker_coordinates, list: List of angles (-180 to 180 for most joints)
    """
    row = int(checker_space[1])-1
    col = ord(checker_space[0].upper()) - ord('A')

    # starting point for coordinates    
    checker_coordinates = [105, -80.5, 140, 180, 0, 0]
    
    # adjust bottom 2 joints
    checker_coordinates[0] = row*23 + checker_coordinates[0]
    checker_coordinates[1] = col*23 + checker_coordinates[1]

    return checker_coordinates

def coord_space_before_after(checker_coordinates):
    """
    Give before and after coordinates based on board level coordinates
    For use with operational space

    Args:
        checker_coordinates, list: Operational space on checkerboard

    Returns:
        checker_coordinates_ba, list: Operational space on checkerboard just above input
    """
    checker_coordinates_ba = checker_coordinates.copy()
    checker_coordinates_ba[2] += 15


    return checker_coordinates_ba

def coord_move(mc, checker_space, sleep_time, magnet="off"):
    """
    Give movements based on entered checker space
    For use with operational space

    Args:
        mc, object: MyCobot object
        checker_space, str: Space on checkerboard (ex. a7)
        sleep_time, int: Rest time between robot movements
        magnet, str: Electromagnet relay setting

    Returns:
        None
    """
    # get coordinates
    coords = convert_to_coords(checker_space)
    coords_ba = coord_space_before_after(coords)

    #movements
    mc.send_coords(coords_ba, speed, 0)
    sleep(sleep_time)
    mc.send_coords(coords, speed, 0)
    sleep(sleep_time)
    electromagnet(relay=magnet)
    sleep(1)
    mc.send_coords(coords_ba, speed, 0)
    sleep(sleep_time)



if __name__ == "__main__":
    # Setup
    mc = MyCobot("/dev/ttyAMA0", 1000000) # startup robot
    speed = 25 # set speed
    starting_angles = [0, 0, 0, 0, 0, 0]  # starting location, up in air
    mc.send_angles(starting_angles, speed)
    sleep(1)

    # move to a1
    coord_move(mc, checker_space="a1", sleep_time=1)

    while True:
        checker_space = input('Enter the checkerspace (ex. A3): ')

        # top numbers (8's)
        if checker_space[0].lower() in "abcdefgh" and int(checker_space[1]) == 8:
            angle_move(mc, checker_space, sleep_time=3, magnet="on")
        
        # numbers 1-7
        elif checker_space[0].lower() in "abcdefgh" and int(checker_space[1]) in range(1,8):
            coord_move(mc, checker_space, sleep_time=3, magnet="on")
        
        # invalid move
        else:
            print("Space not on board, try again")
            continue

        # reset move to a1
        coord_move(mc, checker_space="a1", sleep_time=1)
