import cv2
import numpy as np

def process_color(image, lower, upper, color_name):
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

            # Optionally, draw the circle and center on the image
            # cv2.circle(image, center, int(radius), (0, 255, 0), 2)
            # cv2.circle(image, center, 2, (0, 0, 255), -1)
            # cv2.putText(image, color_name, (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return centers

if __name__ == "__main__":
    # Load the image
    image = cv2.imread("images/test_image.jpg")

    # save the image
    cv2.imwrite("images/test_image_2.jpg", image)

    # Check if the image was loaded properly
    if image is None:
        print("Error: Could not load image.")
        exit()

    # Create a copy of the image to draw on
    output_image = image.copy()

    # Define the HSV ranges for orange, green, and pink
    # Orange color range 
    # RGB of 242, 120, 7
    lower_orange = (12, 200, 200)
    upper_orange = (18, 255, 255)

    # Green color range 
    # RGB of 3, 108, 76
    lower_green = (76, 100, 100)
    upper_green = (86, 255, 255)

    # Pink color ranges (due to hue wrapping)
    lower_pink1 = (160, 100, 100)
    upper_pink1 = (179, 255, 255)
    lower_pink2 = (0, 100, 100)
    upper_pink2 = (10, 255, 255)

    # Process each color and find centers
    centers_orange = process_color(image, lower_orange, upper_orange, "Orange")
    centers_green = process_color(image, lower_green, upper_green, "Green")
    centers_pink1 = process_color(image, lower_pink1, upper_pink1, "Pink")
    centers_pink2 = process_color(image, lower_pink2, upper_pink2, "Pink")
    centers_pink = centers_pink1 + centers_pink2  # Combine both pink ranges

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

    print("\nPink centers:")
    for center in centers_pink:
        print(center)
        cv2.circle(output_image, center, 5, (255, 0, 255), -1)  # BGR color for pink
        cv2.putText(output_image, 
                    "Pink", 
                    (center[0]+10, center[1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (255, 0, 255), 
                    2
                    )

    # Save the output image with centers marked
    cv2.imwrite("images/filtered_image_with_centers.jpg", output_image)