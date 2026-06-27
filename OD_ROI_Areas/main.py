import cv2
import numpy as np
from ultralytics import YOLO
import cvzone

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
# Load COCO class names

# Load the YOLOv8 model
model = YOLO("yolo11s.pt")
names = model.names
# Open the video file (use video file or webcam, here using webcam)
cap = cv2.VideoCapture('pcount.mp4')
count = 0

# Define the area of interest (ROI) polygon
area = [(524, 282), (152, 331), (243, 459), (834, 427)]

# Define the codec and create VideoWriter object
frame_width, frame_height = 1020, 500
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (frame_width, frame_height))

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % 2 != 0:
        continue

    frame = cv2.resize(frame, (frame_width, frame_height))
    
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True)

    # Check if there are any boxes in the results
    if results[0].boxes is not None and results[0].boxes.id is not None:
        # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
        boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
        class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
        track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
        confidences = results[0].boxes.conf.cpu().tolist()  # Confidence score
        for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
            c = names[class_id]
            if 'person' in c:
                x1, y1, x2, y2 = box
                cx = int(x1 + x2) // 2
                cy = int(y1 + y2) // 2
                result = cv2.pointPolygonTest(np.array(area,np.int32), (cx, cy), False)
                if result >= 0:
                    # cv2.circle(frame, (cx, cy), 1, (255, 0, 255), -1)
                    # cv2.rectangle(frame,(x1, y1),(x2, y2),(0, 255, 0), 1)
                    cvzone.putTextRect(frame, f'{c}',(x1, y1), 1, 1, (255, 255, 0), 1)
                        
 
    cv2.polylines(frame, [np.array(area,np.int32)], True, color=(0, 255, 255), thickness=1)
    cv2.imshow("RGB", frame)

    # Write the frame to the output video
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
       break

# Release the video capture and writer objects and close the display window
cap.release()
out.release()
cv2.destroyAllWindows()