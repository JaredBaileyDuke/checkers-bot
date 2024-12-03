import cv2
import numpy as np

def detect_apriltags(image_path):
    """
    Detect AprilTags in an image.
    
    Args:
        image_path (str): Path to the input image.

    Returns:
        None
    """
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not load image.")
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

    # Draw detected markers
    output_image = cv2.aruco.drawDetectedMarkers(image.copy(), corners, ids)

    if ids is not None:
        print(f"Detected AprilTag IDs: {ids.flatten()}")
        for i, center in enumerate(corners):
            # Calculate the center of each detected AprilTag
            center_point = np.mean(center[0], axis=0)
            # Print the center point
            print(f"AprilTag {ids.flatten()[i]} center: {center_point}")
            # Draw a dot at the center point
            cv2.circle(output_image, (int(center_point[0]), int(center_point[1])), 5, (0, 255, 0), -1)
    else:
        print("No AprilTags detected.")

    # Save and display the result
    cv2.imwrite("sample_images/detected_apriltags.jpg", output_image)


if __name__ == "__main__":
    detect_apriltags("sample_images/15.jpg")
