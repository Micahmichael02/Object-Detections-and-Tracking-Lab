import cv2
import numpy as np
import matplotlib.pyplot as plt
from ulitl import get_parking_spots_bboxes, empty_or_not

def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))

# Paths for mask and video
mask_path = r"C:\Users\user\OneDrive\Documents\Computer Vision\Beginner_projects\parking_spot_detection\mask_1920_1080.png"
video_path = r"C:\Users\user\OneDrive\Documents\Computer Vision\Beginner_projects\parking_spot_detection\data\parking_1920_1080_loop.mp4"
output_path = "parking_detection_output.mp4"

# Load the mask and video
mask = cv2.imread(mask_path, 0)
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Set up the VideoWriter for saving output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Getting the bounding boxes from the mask using cv2
connect_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
spots = get_parking_spots_bboxes(connect_components)
print(f"Parking spots: {len(spots)}")

frame_num = 0
spots_status = [None for _ in spots]
diffs = [None for _ in spots]
previous_frame = None
ret = True
step = 30

try:
    while ret:
        ret, frame = cap.read()

        if not ret:
            break

        # Analyze frames at specific intervals
        if frame_num % step == 0 and previous_frame is not None:
            for spot_indx, spot in enumerate(spots):
                x1, y1, w, h = spot
                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]
                diffs[spot_indx] = calc_diff(spot_crop, previous_frame[y1:y1 + h, x1:x1 + w, :])

        if frame_num % step == 0:
            if previous_frame is None:
                arr_ = range(len(spots))
            else:
                arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4][::-1]
            for spot_indx in arr_:
                spot = spots[spot_indx]
                x1, y1, w, h = spot
                spot_crop = frame[y1:y1 + h, x1:x1 + w, :]
                spot_status = empty_or_not(spot_crop)
                spots_status[spot_indx] = spot_status

        if frame_num % step == 0:
            previous_frame = frame.copy()

        # Draw rectangles and update the frame
        for spot_indx, spot in enumerate(spots):
            spot_status = spots_status[spot_indx]
            x1, y1, w, h = spots[spot_indx]

            if spot_status:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
            else:
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)

        cv2.putText(frame, f'Available spots: {sum(spots_status)} / {len(spots_status)}', 
                    (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Save the frame to the output video
        out.write(frame)

        # Display the frame
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.imshow("frame", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        frame_num += 1
except KeyboardInterrupt:
    print("Recording stopped by user.")
finally:
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
