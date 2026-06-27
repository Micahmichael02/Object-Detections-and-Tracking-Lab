import cv2
import numpy as np
import pickle
import pandas as pd
from ultralytics import YOLO
import cvzone

# Load saved polylines and area names
with open('freedomtech', 'rb') as f:
    data = pickle.load(f)
    polylines, area_name = data['polylines'], data['area_name']

# Load class names
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# Load YOLO model
model = YOLO('yolo11n.pt')

# Capture video
cap = cv2.VideoCapture(r"C:\Users\user\OneDrive\Documents\Computer Vision\Beginner_projects\yolo_parking_space\easy1.mp4")

# Set up video writer for .mp4
frame_width = 1020  # Resized width
frame_height = 500  # Resized height
fps = int(cap.get(cv2.CAP_PROP_FPS))
output_path = "output_with_detections.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        count += 1
        if count % 3 != 0:
            continue

        frame = cv2.resize(frame, (1020, 500))
        frame_copy = frame.copy()
        results = model.predict(frame)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")
        list1 = []

        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])

            c = class_list[d]
            cx = int(x1 + x2) // 2
            cy = int(y1 + y2) // 2
            if 'car' in c:
                list1.append([cx, cy])

        counter1 = []
        list2 = []
        for i, polyline in enumerate(polylines):
            list2.append(i)
            cv2.polylines(frame, [polyline], True, (0, 255, 0), 1)
            cvzone.putTextRect(frame, f'{area_name[i]}', tuple(polyline[0]), 1, 1)
            for i1 in list1:
                cx1 = i1[0]
                cy1 = i1[1]
                result = cv2.pointPolygonTest(polyline, (cx1, cy1), False)
                if result >= 0:
                    cv2.circle(frame, (cx1, cy1), 1, (255, 0, 0), -1)
                    cv2.polylines(frame, [polyline], True, (0, 0, 255), 1)
                    counter1.append(cx1)

        car_count = len(counter1)
        free_space = len(list2) - car_count
        cvzone.putTextRect(frame, f'car count: {car_count}', (30, 30), 1, 1)
        cvzone.putTextRect(frame, f'freespace: -{free_space}', (30, 70), 1, 1)
        print(car_count)

        # Write the frame to the video file
        out.write(frame)

        # Display the frame
        cv2.imshow('FRAME', frame)
        key = cv2.waitKey(1) & 0xFF
except KeyboardInterrupt:
    print("Recording stopped by user.")
finally:
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
