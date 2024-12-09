import cv2
import os
from time import sleep
from . import piece_locations as pl


def return_piece_location_string(input):
    """
    Convert the piece locations to the expected output format.
    Args:
        input (list): List of piece location info. ["a4", (725, 98), "Orange", True]
    Returns:
        str: Piece location in the expected format. "RA4K"
    """
    answer = ""
    answer += "R" if input[2] == "Orange" else "B"
    answer += input[0].upper()
    answer += "K" if input[3] else ""
    return answer

def return_board_layout(piece_locations):
    '''
    Convert the piece locations to the expected output format

    Args:
        piece_locations (dict): Dictionary of piece locations and details

    Returns:
        list: List of expected output format. ["RA4K", "BA3", ...]
    '''
    # Convert the piece locations to the expected output format
    piece_location_list = []
    for location, details in piece_locations.items():
        piece_location_list.append(return_piece_location_string([location, details[0], details[1], details[2]]))
    return piece_location_list

def ask_for_king(piece_location, piece_locations):
    '''
    Find if the piece is a King

    Args:
        piece_location (str): The location of the piece (a4, b3, etc.)
        piece_locations (dict): Dictionary of piece locations and details

    Returns:
        bool: True if the piece is a King, False otherwise
    '''
    # Check if the piece is a King
    #see if the piece location is in the dictionary
    if piece_location not in piece_locations:
        return False
    print(piece_locations[piece_location])
    return piece_locations[piece_location][2]

def cv_process_image(image):
    '''
    Process the image to detect the piece locations
    '''
    # Check if the image was loaded properly
    if image is None:
        print("Error: Could not load image.")
        exit()

    original_image = image.copy()

    # Check for misalignment of original image
    if pl.misalignment_alert(original_image):
        print("Error: Image is misaligned.")
        exit()

    # Find the AprilTags in the original image
    center_points = pl.detect_apriltags(original_image)

    # Rotate the image so that AprilTags align vertically
    rotated_image = pl.rotate_image(original_image, center_points)

    # Check for misalignment of rotated image
    if pl.misalignment_alert(rotated_image):
        print("Error: Rotated image is misaligned.")
        exit()

    # Find the AprilTags in the rotated image
    center_points = pl.detect_apriltags(rotated_image)

    # Find the center of each board square
    board_square_centers = pl.find_board_square_centers(rotated_image, center_points)

    # Return the squares occupied by each piece
    piece_locations = pl.return_piece_locations(rotated_image, board_square_centers)

    # Print the piece locations
    for location, details in piece_locations.items():
        print(location, details[0], details[1], details[2])

    return piece_locations

def initialize_webcam():
    '''
    Initialize the webcam
    '''
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # Allow the camera to warm up
    sleep(2)

    # Discard initial frames to allow auto-adjustments
    for _ in range(5):
        cap.read()

    return cap

def capture_frame(cap):
    '''
    Capture a frame from the webcam
    '''
    # Capture a frame
    ret, frame = cap.read()

    # Check if the frame was captured properly
    if not ret:
        print("Error: Could not capture frame.")
        return None

    return frame

def display_feed():
    '''
    Display the webcam feed and capture images
    '''
    # Initialize the webcam
    cap = initialize_webcam()

    print("Press 's' to take a snapshot or 'q' to quit.")
    while True:
        # Capture a frame
        frame = capture_frame(cap)
        delay = 10 * 1000 #the delay is in milliseconds

        # Display the frame
        try:
            piece_locations = cv_process_image(frame)
            delay = 1 * 1000 #the delay is in milliseconds
        except:
            print("Error: Could not process image.")
            cv2.imshow('Empty Webcam Feed', frame)
            delay = 1 * 1000 

        # Wait for a key press, delay for live feed
        key = cv2.waitKey(delay) & 0xFF

        # If 's' is pressed, capture a photo
        if key == ord('s'):
            # Define the path to save the image
            path = os.path.join("images", "snapshot.jpg")
            cv2.imwrite(path, frame)
            print(f"Photo saved at {path}")

        # If 'q' is pressed, quit the feed
        elif key == ord('q'):
            print("Exiting...")
            break

    # Release the webcam and close any open windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Ensure the images directory exists
    if not os.path.exists('images'):
        os.makedirs('images')

    # Display webcam feed and capture images
    display_feed()
