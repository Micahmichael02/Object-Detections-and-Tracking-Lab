import os

import cv2

# Create a directory to store the data
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Number of classes and the size of the dataset
number_of_classes = 3
dataset_size = 100

# Collect data
cap = cv2.VideoCapture(0)

# Set the resolution of the video capture
for j in range(number_of_classes):
    # Create a directory for each class
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    # Print the class number
    print('Collecting data for class {}'.format(j))

    # Wait for the user to press 'q' to start collecting data
    done = False
    # Show the message on the screen
    while True:
        ret, frame = cap.read() # Read the frame
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA) # Display the message
        cv2.imshow('frame', frame) # Show the frame
        if cv2.waitKey(25) == ord('q'): # If the user presses 'q'
            break # Break the loop

    # Collect the data
    counter = 0
    while counter < dataset_size: # While the number of collected images is less than the dataset size
        ret, frame = cap.read()
        cv2.imshow('frame', frame) # Show the frame
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame) # Save the image

        counter += 1 # Increment the counter

cap.release()
cv2.destroyAllWindows()