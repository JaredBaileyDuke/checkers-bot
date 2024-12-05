"""
Functions for detecting AprilTags in an image and rotating the image to align the tags vertically.

detect_apriltags(image) - Detect AprilTags in an image.
rotate_image(image, center_points) - Rotate image so that AprilTags align vertically.
misalignment_alert(image) - Check for misalignment of rotated image which fails to meet the 3 AprilTag 
    requirement.
"""

import cv2
import numpy as np

def detect_apriltags(image):
    """
    Detect AprilTags in an image.
    
    Args:
        image (str): Image of checkerboard pattern with AprilTags.

    Returns:
        center_points (dict): Dictionary of AprilTag number (int) and center points (x, y).
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the AprilTag dictionary and detector parameters
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
    parameters = cv2.aruco.DetectorParameters()

    # Adjust detection parameters for small tags
    parameters.adaptiveThreshWinSizeMin = 3
    parameters.adaptiveThreshWinSizeMax = 23
    parameters.adaptiveThreshWinSizeStep = 10
    parameters.minMarkerPerimeterRate = 0.02
    parameters.maxMarkerPerimeterRate = 4.0
    parameters.polygonalApproxAccuracyRate = 0.05

    # Create the detector
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    center_points = {}
    if ids is not None:
        for i in range(len(ids)):
            # Get the center of the marker
            center = np.mean(corners[i][0], axis=0)
            center = (int(center[0]), int(center[1]))
            center_points[int(ids[i][0])] = center

    return center_points

def rotate_image(image, center_points):
    """
    Rotate image so that AprilTags align vertically.
    
    Args:
        image (np.ndarray): The original image.
        center_points (dict): Dictionary of AprilTag number (int) and center points (x, y).

    Returns:
        np.ndarray: The rotated image.
    """
    if 4 in center_points and 22 in center_points:
        first = 4
        second = 22
    elif 10 in center_points and 16 in center_points:
        first = 10
        second = 16

    # Determine the angle of rotation
    x_offset = center_points[first][0] - center_points[second][0]
    y_offset = center_points[first][1] - center_points[second][1]
    angle = np.arctan2(y_offset, x_offset) * 180 / np.pi + 90

    # Rotate the image
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return rotated_image

def misalignment_alert(image):
    """
    Check for misalignment of rotated image which fails to meet the 3 AprilTag requirement.
    
    Args:
        image (np.ndarray): The image.

    Returns:
        bool: True if the image is misaligned, False otherwise.
    """
    center_points = detect_apriltags(image)

    if len(center_points) < 3:
        return True
    return False




if __name__ == "__main__":
    # Load the image
    image = cv2.imread("sample_images/5.jpg")

    # Check if the image was loaded properly
    if image is None:
        print("Error: Could not load image.")
        exit()

    center_points = detect_apriltags(image)

    if center_points:
        print(center_points)

        # Display the image with AprilTag centers
        output_image = image.copy()
        for center in center_points.values():
            cv2.circle(output_image, center, 5, (0, 255, 0), -1)

        cv2.imshow("AprilTag Centers", output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Rotate the image
        rotated_image = rotate_image(output_image, center_points)

        # Display the rotated image
        cv2.imshow("Rotated Image", rotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        
