import cv2
import numpy as np

def detect_apriltags(image):
    """
    Detect AprilTags in an image.
    
    Args:
        image (str): Image of checkerboard pattern with AprilTags.

    Returns:
        None
    """
    # Load the image
    image = cv2.imread(image)

    if image is None:
        return

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

    center_points = []
    if ids is not None:
        for i, center in enumerate(corners):
            # Calculate the center of each detected AprilTag
            center_point = np.mean(center[0], axis=0)
            center_point = (int(center_point[0]), int(center_point[1]))
            center_points.append(center_point)
    else:
        print("No AprilTags detected.")

    return center_points


if __name__ == "__main__":
    center_points = detect_apriltags("sample_images/15.jpg")

    if center_points:
        print(center_points)
