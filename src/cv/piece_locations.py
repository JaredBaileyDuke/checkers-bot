"""
Result: Find the locations (a4, b3, etc.) of all the pieces on the checkbaordboard.

First find the board square centers (x, y) by:
- Find the AprilTags in the image.
  - 4 AprilTags around the board, one in near each corner.
- Find the center of each AprilTag.
- Rotate the image so that the AprilTags align vertically.
- Repeat the AprilTag detection and center finding.
- Use 2 diagonal AprilTags to find the board orientation and spacing, noting the center of each board square.
  - Done by finding the distance between the centers of the 2 AprilTags,
    and applying a percentage of that distance to the center of each board square.
  - The other 2 AprilTags are redundant, and used as such.

Second find the piece locations and colors, using the hsv.py script.

Third return the squares occupied by each piece.
    - Compare the piece locations to the board square centers.
"""

import cv2
import numpy as np
from math import sqrt
from .hsv import *
from .april_tags import *

def find_board_square_centers(image, center_points, hold_display=False):
    """
    Find the center of each board square.

    Args:
        image (np.ndarray): The rotated image.
        center_points (dict): Dictionary of AprilTag number (int) and center points (x, y).
        hold_display (bool): Whether to hold the display window open.

    Returns:
        List of tuples: List of center points (x, y) for each board square.
    """
    # Cover redundant cases
    if 4 in center_points and 16 in center_points: # Diagonal case 1
        first = 4
        second = 16
        x_perc = 0.1205
        y_perc = 0.1275
        first_case = 1
    elif 10 in center_points and 22 in center_points: # Diagonal case 2
        first = 22
        second = 10
        x_perc = 0.1205
        y_perc = 0.1275
        first_case = 0
    else:
        print("Error: Could not find 2 AprilTags for board orientation.")
        return

    # Find the distance between the centers of the 2 AprilTags
    first_center = center_points[first]
    second_center = center_points[second]

    x_distance = abs(first_center[0] - second_center[0])
    y_distance = abs(first_center[1] - second_center[1])

    # Set the square centers to (0, 0) for now
    board_square_centers = {}
    name_list = [
        "a2", "a4", "a6", "a8",
        "b1", "b3", "b5", "b7",
        "c2", "c4", "c6", "c8",
        "d1", "d3", "d5", "d7",
        "e2", "e4", "e6", "e8",
        "f1", "f3", "f5", "f7",
        "g2", "g4", "g6", "g8",
        "h1", "h3", "h5", "h7"
    ]
    
    for name in name_list:
        board_square_centers[name] = (0, 0)

    # Calculate the center of each board square
    if first_case == 1: # Diagonal case 1
        col_count = 0
        row_count = 1
        general_count = 0
        for name in name_list:
            loc = (int(first_center[0] + x_distance * (0.04 + (7 - row_count) * x_perc)),
                        int(first_center[1] + y_distance * (0.03 + col_count * y_perc)))
            board_square_centers[name] = loc

            # Increment row and column counts
            general_count += 1
            row_count += 2
            if row_count == 9:
                row_count = 0
                col_count += 1
            elif row_count == 8:
                row_count = 1
                col_count += 1

    else: # Diagonal case 2
        col_count = 7
        row_count = 1
        general_count = 0
        for name in name_list:
            loc = (int(first_center[0] + x_distance * (0.04 + (7 - row_count) * x_perc)),
                        int(first_center[1] - y_distance * (0.03 + col_count * y_perc)))
            board_square_centers[name] = loc

            # Increment row and column counts
            general_count += 1
            row_count += 2
            if row_count == 9:
                row_count = 0
                col_count -= 1
            elif row_count == 8:
                row_count = 1
                col_count -= 1
        
   
    # Draw circles at the center of each board square
    for name, loc in board_square_centers.items():
        square = (int(loc[0]), int(loc[1]))
        cv2.circle(image, square, 5, (0, 255, 0), -1)

    # Display the image
    cv2.imshow("Board Square Centers", image)
    if hold_display:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return board_square_centers

def return_piece_locations(rotated_image, board_square_centers):
    """
    Return the squares occupied by each piece (a4, b3, etc.).

    Args:
        rotated_image (np.ndarray): The rotated image.
        board_square_centers (list): List of center points (x, y) for each board square.

    Returns:
        dict: Dictionary of piece locations (str) and tuple of center points (x, y), color (str).
    """
    centers_orange = process_color(rotated_image, "Orange")
    centers_green = process_color(rotated_image, "Green")
    centers_purple = process_color(rotated_image, "Purple")

    # Create a dictionary of piece locations and center points
    piece_locations = {}

    # Compare the piece locations to the board square centers
    for color, centers in zip(["Orange", "Green"], [centers_orange, centers_green]):
        for center in centers:
            # Find the closest board square center
            min_distance = float("inf")
            closest_square = None
            square_name = ""
            for name, loc in board_square_centers.items():
                # Calculate the Euclidean distance
                distance = sqrt((center[0] - loc[0])**2 + (center[1] - loc[1])**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_square = loc
                    square_name = name

            # Add the piece location to the dictionary
            piece_locations[square_name] = [closest_square, color, False] # True for King

    # Find the purple pieces (Kings)
    for center in centers_purple:
        # Find the closest board square center
        min_distance = float("inf")
        closest_square = None
        square_name = ""
        for name, loc in board_square_centers.items():
            # Calculate the Euclidean distance
            distance = sqrt((center[0] - loc[0])**2 + (center[1] - loc[1])**2)
            if distance < min_distance:
                min_distance = distance
                closest_square = loc
                square_name = name

        # Add the King designation to the dictionary
        try:
            piece_locations[square_name][2] = True
        except KeyError:
            print("Error: Could not find a matching piece location for the King.")

    return piece_locations

if __name__ == "__main__":
    # Load the image
    image = cv2.imread("sample_images/30.jpg")

    if image is None:
        print("Error: Could not load image.")
        exit()

    original_image = image.copy()

    # Check for misalignment of original image
    if misalignment_alert(original_image):
        print("Error: Image is misaligned.")
        exit()

    # Find the AprilTags in the original image
    center_points = detect_apriltags(original_image)

    # Rotate the image so that AprilTags align vertically
    rotated_image = rotate_image(original_image, center_points)

    # Check for misalignment of rotated image
    if misalignment_alert(rotated_image):
        print("Error: Rotated image is misaligned.")
        exit()

    # Find the AprilTags in the rotated image
    center_points = detect_apriltags(rotated_image)

    # Find the center of each board square
    board_square_centers = find_board_square_centers(rotated_image, center_points, hold_display=True)

    # Return the squares occupied by each piece
    piece_locations = return_piece_locations(rotated_image, board_square_centers)
    
    # Print the piece locations
    for location, details in piece_locations.items():
        print(location, details[0], details[1], details[2])