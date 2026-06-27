import cv2
import argparse 
import os
import mediapipe as mp

output_dir = "./blurred_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# read image
img_path = r"./img1.jpg"


def process_img(img, face_detection):
    # convert the image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    H, W, _ = img.shape

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x1 = int(x1 * W)
            y1 = int(y1 * H)
            w = int(w * W)
            h = int(h * H)

            # img = cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)

            # blur faces
            img[y1:y1 + h, x1:x1 + w,:] = cv2.blur(img[y1:y1 + h, x1:x1 + w,:], (80, 80))

 
    return img

argparse = argparse.ArgumentParser()

argparse.add_argument("--mode", default='video')
argparse.add_argument("--filepath", default="./img1.jpg") # path to image or video

args = argparse.parse_args()

# detect faces
mp_face_detection  = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    
    # read image
    if args.mode == 'image':
        img = cv2.imread(args.filepath)

        img = process_img(img, face_detection)
    
        # save image
        cv2.imwrite(os.path.join(output_dir, "blurred_img.jpg"), img)

    elif args.mode == 'video': # read video

        cap = cv2.VideoCapture(args.filepath) # read video
        ret, frame = cap.read() # read first frame

        output_video = cv2.VideoWriter(os.path.join(output_dir, "blurred_video.mp4"),  # save video
                                       cv2.VideoWriter_fourcc(*'mp4v'), # codec
                                       30, # fps
                                       (frame.shape[1], frame.shape[0])) # save video

        while ret:
            frame = process_img(frame, face_detection) # process frame
            ret, frame = cap.read() # read next frame
            output_video.write(frame)  # save frame
            cap.release() # release video
            output_video.release() # save video
            
# cv2.imshow("output.jpg", img)
# cv2.waitKey(0)