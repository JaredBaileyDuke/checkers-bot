import cv2
import os
from time import sleep

def take_photo(path):
    # Initialize the webcam
    cap = cv2.VideoCapture(1)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # Allow the camera to warm up
    sleep(2)

    # Discard initial frames to allow auto-adjustments
    for _ in range(5):
        cap.read()

    # Set camera properties
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # 0.75 is auto mode; set to 0.25 for manual
    cap.set(cv2.CAP_PROP_EXPOSURE, -6)  # Adjust exposure level as needed

    # Capture a frame
    ret, frame = cap.read()

    # Check if the frame was captured properly
    if not ret:
        print("Error: Could not capture frame.")
        exit()

    # Display the captured image (for debugging)
    cv2.imshow('Captured Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the image
    cv2.imwrite(path, frame)

    # Release the webcam
    cap.release()

    print(f"Photo saved at {path}")

if __name__ == "__main__":
    # Ensure the images directory exists
    if not os.path.exists('images'):
        os.makedirs('images')

    # Define the path to save the image
    path = os.path.join("images", "test_image_2.jpg")

    # Take a photo
    take_photo(path)
