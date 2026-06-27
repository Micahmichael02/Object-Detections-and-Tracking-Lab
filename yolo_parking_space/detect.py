import cv2
import numpy as np
import cvzone
import pickle

cap = cv2.VideoCapture(r"C:\Users\user\OneDrive\Documents\Computer Vision\Beginner_projects\yolo_parking_space\easy1.mp4")

drawing = False
area_name = []
try:
    with open('freedomtech', 'rb') as f:
            data = pickle.load(f)
            polylines, area_name = data['polylines'], data['area_name']
except:
    polylines = []

points = []

current_name = ""

def draw(event, x, y, flags, param):
    global points, drawing, current_name
    drawing = True
    if event == cv2.EVENT_LBUTTONDOWN:
        points=[(x,y)]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        current_name = input("Enter the name of the area: ")
        if current_name != "":
            area_name.append(current_name)
            polylines.append(np.array(points, np.int32))
              
while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame=cv2.resize(frame,(1020,500))
    for i, polyline in  enumerate(polylines):
        print(i, current_name)
        cv2.polylines(frame, [polyline], True, (0, 255, 0), 1)
        # Add the color argument (BGR format) for the text
        cvzone.putTextRect(frame, f'{area_name[i]}', tuple(polyline[0]),1, 1)
        # cv2.putText(frame, f'{area_name[i]}', tuple(polyline[0]), cv2.FONT_HERSHEY_SIMPLEX, 
                    # 1, (255, 0, 0), 1)  # Blue color, thickness 2
        
    cv2.imshow('FRAME', frame)
    cv2.setMouseCallback('FRAME', draw)
    Key = cv2.waitKey(100) & 0xFF
    if Key == ord('s'):
        with open('freedomtech', 'wb') as f:
            data = {'polylines': polylines, 'area_name': area_name}
            pickle.dump(data, f)
    elif Key == 27:  # Press 'ESC' to exit
        break
    
cap.release()
cv2.destroyAllWindows()