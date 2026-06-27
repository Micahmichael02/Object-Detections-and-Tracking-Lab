import cv2
import util
import numpy as np
from util import get_car
from util import read_license_plate, write_csv
from sort.sort import *
from ultralytics import YOLO

results = {}

mot_tracker = Sort()

# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO(r"C:\Users\user\OneDrive\Documents\Computer Vision\Beginner_projects\plate_no_detection\Anpr_YOLOv8_EasyOCR\license_plate_detector.pt")

# load video
cap = cv2.VideoCapture(r'./tc1.mp4')

vehicles = [2, 3, 5, 7]  # car, bus, truck, motorbike

# read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        # if frame_nmr > 200:
        #     break
        results[frame_nmr] = {}
        # detect vehicles
        detections = coco_model(frame)[0]
        detections_boxes = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_boxes.append([x1, y1, x2, y2, score])

        # track vehicles
        track_ids = mot_tracker.update(np.asarray(detections_boxes))
        
        # detect license plates
        license_plate_detections = license_plate_detector(frame)[0]
        for license_plate in license_plate_detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # assign license plates to vehicles
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)
            print(f"Frame {frame_nmr} - License Plate Detection: {license_plate}")

            if car_id != -1:
                # crop license plates
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :] 
                # cv2.imwrite(f'license_plate_crop_frame_{frame_nmr}_car_{car_id}.jpg', license_plate_crop)
                # print(f"Frame {frame_nmr} - Car ID {car_id}: Cropped License Plate Saved")

                # process license plates
                license_plate_crop_grey = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_grey, 64, 255, cv2.THRESH_BINARY_INV)

                # read license plates numbers
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                    'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                    'text': license_plate_text,
                                                                    'bbox_score': score,
                                                                    'text_score': license_plate_text_score}}
                    print(f"Frame {frame_nmr} - Car ID {car_id}: License Plate Detected - {license_plate_text}")
                else:
                    # Handle the case where no valid license plate is detected
                    print(f"No valid license plate detected in frame {frame_nmr} for car ID {car_id}.")

# save results
write_csv(results, './results.csv')