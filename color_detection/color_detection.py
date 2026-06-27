import cv2
from PIL import Image  # Used for finding bounding boxes
from util import get_limits  # Import the utility function for HSV limits

# Defining the target color in BGR format (yellow) 
yellow = [0, 255, 255]

# Initialize video capture from the default webcam
cap = cv2.VideoCapture(0)

# Main loop for processing video frames
while True:
    ret, frame = cap.read()  # Capturing a frame from the webcam

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Converting the frame to HSV

    lowerLimit, upperLimit = get_limits(color=yellow)  # Getting HSV limits for yellow

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)  # Creating a binary mask for the color range

    mask_ = Image.fromarray(mask)  # Converting the mask to a PIL image

    bbox = mask_.getbbox()  # Finding the bounding box of the detected color region

    if bbox is not None:  # If a bounding box is found
        x1, y1, x2, y2 = bbox  # Extracting the coordinates of the bounding box
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)  # Drawing a green rectangle

    cv2.imshow('frame', mask)  # Displaying the mask in a window

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exiting the loop when 'q' is pressed
        break

cap.release()  # Releasing the webcam
cv2.destroyAllWindows()  # Closeing all OpenCV windows
