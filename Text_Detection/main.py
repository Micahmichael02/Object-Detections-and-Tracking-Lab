import cv2
import easyocr
import numpy as np
import matplotlib.pyplot as plt
import os

# Read the image
image_path = r'dataset/test3.png'
img = cv2.imread(image_path)

# instance text detection
reader = easyocr.Reader(['en'], gpu=False)

# Detect text in the image
text = reader.readtext(img)

threshold = 1.0

if img is None:
    print(f"Failed to load image at {image_path}. Please check the file path and integrity.")
else:
    try:
        # Instance text detection
        reader = easyocr.Reader(['en'], gpu=False)

        # Detect text in the image
        text = reader.readtext(img)

        print(text)

        # Draw bounding box around text (optional)
        for (bbox, text, prob) in text:
            if prob < threshold:
                # continue
                # Unpack the bounding box
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))

                # Draw the bounding box on the image
                img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

                # Add the text to the image 
                img = cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display the image with bounding boxes
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

    except ValueError as e:
        print(f"Error during text detection: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
