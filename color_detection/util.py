import numpy as np
import cv2

# Function is to calculate HSV limits for a given BGR color
def get_limits(color):
    c = np.uint8([[color]])  # Creating a numpy array for the BGR color
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)  # Converting BGR to HSV

    hue = hsvC[0][0][0]  # Extracting the hue value from the HSV color

    # Handling special cases for red hue (wrap-around on the HSV scale)
    if hue >= 165:  # If the hue is near the upper limit for red
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # If the hue is near the lower limit for red
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        # General case for other colors
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit
