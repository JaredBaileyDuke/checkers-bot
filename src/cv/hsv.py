"""
Functions to process an image and find objects of a specific color using HSV color space.

process_color(image, lower, upper, color_name) - Process the image to find objects of a specific color 
    and compute their center points.

"""

import cv2
import numpy as np

def process_color(image, color_name):
    """
    Process the image to find objects of a specific color and compute their center points.

    Args:
        image (np.ndarray): The original image.
        lower (tuple): The lower HSV bound.
        upper (tuple): The upper HSV bound.
        color_name (str): Name of the color (for labeling).

    Returns:
        List of tuples: List of center points (x, y) for detected objects.
    """
    # Lower case the color name
    color_name = color_name.lower()

    # Define the HSV ranges for orange and green
    if color_name == "orange":
        lower = (10, 120, 120)
        upper = (20, 255, 255)
    elif color_name == "green":
        lower = (76, 100, 100)
        upper = (86, 255, 255)
    elif color_name == "purple":
        lower = (125, 50, 50)
        upper = (150, 200, 200)

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create mask for the color
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = []

    for contour in contours:
        # Skip small contours that might be noise
        if cv2.contourArea(contour) > 100:
            # Use cv2.minEnclosingCircle to get center and radius
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            centers.append(center)

    return centers

if __name__ == "__main__":
    # Load the image
    image = cv2.imread("sample_images/30.jpg")

    # Check if the image was loaded properly
    if image is None:
        print("Error: Could not load image.")
        exit()

    # Create a copy of the image to draw on
    output_image = image.copy()

    # Process each color and find centers
    centers_orange = process_color(image, "Orange")
    centers_green = process_color(image, "Green")
    centers_purple = process_color(image, "Purple")

    # Print and annotate the centers for each color
    print("Orange centers:")
    for center in centers_orange:
        print(center)
        cv2.circle(output_image, center, 5, (7, 120, 242), -1)  # BGR color for orange
        cv2.putText(output_image, 
                    "Orange", 
                    (center[0]+10, center[1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (7, 120, 242), 
                    2
                    )

    print("\nGreen centers:")
    for center in centers_green:
        print(center)
        cv2.circle(output_image, center, 5, (76, 108, 3), -1)  # BGR color for green
        cv2.putText(output_image, 
                    "Green", 
                    (center[0]+10, 
                     center[1]), 
                     cv2.FONT_HERSHEY_SIMPLEX, 
                     0.5, 
                     (76, 108, 3), 
                     2
                     )
        
    print("\nPurple centers:")
    for center in centers_purple:
        print(center)
        cv2.circle(output_image, center, 5, (169, 54, 104), -1)  # BGR color for purple
        cv2.putText(output_image, 
                    "Purple", 
                    (center[0]+10, 
                     center[1]), 
                     cv2.FONT_HERSHEY_SIMPLEX, 
                     0.5, 
                     (169, 54, 104), 
                     2
                     )


    # Save the output image with centers marked
    cv2.imwrite("sample_images/filtered_image_with_centers.jpg", output_image)