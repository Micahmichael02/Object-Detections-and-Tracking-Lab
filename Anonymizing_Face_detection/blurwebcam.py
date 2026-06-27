import cv2
import argparse 
import os
import mediapipe as mp

output_dir = "./blurred_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

            # blur faces
            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w, :], (80, 80))

    return img

argparse = argparse.ArgumentParser()

argparse.add_argument("--mode", default='webcam') # input 'image', 'video', or 'webcam' in the default value
argparse.add_argument("--filepath", default=None)  # path to image or video

args = argparse.parse_args()

# detect faces
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    if args.mode == 'image': # if the mode is 'image'
        if args.filepath is None: # if the filepath is None
            print("Please provide the file path for the image.") # print the message
        else: # if the filepath is not None
            img = cv2.imread(args.filepath) # read the image
            if img is None: # if the image is None
                print(f"Failed to load image at {args.filepath}") # print the message
            else: # if the image is not None
                img = process_img(img, face_detection)  # process the image
                cv2.imwrite(os.path.join(output_dir, "blurred_img.jpg"), img) # save the image

    elif args.mode == 'video': # if the mode is 'video'
        if args.filepath is None: # if the filepath is None
            print("Please provide the file path for the video.") # print the message
        else:   # if the filepath is not None
            cap = cv2.VideoCapture(args.filepath) # read the video
            ret, frame = cap.read() # read the first frame
            
            if not ret: # if the frame is not read
                print(f"Failed to load video at {args.filepath}") # print the message
            else: # if the frame is read
                output_video = cv2.VideoWriter(os.path.join(output_dir, "blurred_video.mp4"), # save the video
                                               cv2.VideoWriter_fourcc(*'mp4v'),  # codec
                                               30, # fps
                                               (frame.shape[1], frame.shape[0])) # save the video

                while ret: # while the frame is read
                    frame = process_img(frame, face_detection) # process the frame
                    output_video.write(frame) # save the frame
                    ret, frame = cap.read() # read the next frame

                cap.release() # release the video
                output_video.release() # save the video

    elif args.mode == 'webcam': # if the mode is 'webcam'
        cap = cv2.VideoCapture(0) # read the webcam
        ret, frame = cap.read() # read the first frame
        output_video = cv2.VideoWriter(os.path.join(output_dir, "blurred_video.mp4"), # save the video
                                               cv2.VideoWriter_fourcc(*'mp4v'),  # codec
                                               25, # fps
                                               (frame.shape[1], frame.shape[0])) # save the video


        while ret: # while the frame is read
            frame = process_img(frame, face_detection) # process the frame
            cv2.imshow("frame", frame) # show the frame

            if cv2.waitKey(25) & 0xFF == ord('q'):  # press 'q' to exit
                break # break the loop

            output_video.write(frame) # save the frame
            ret, frame = cap.read() # read the next frame

        cap.release() # release the webcam
        cv2.destroyAllWindows() # close the window

    else: # if the mode is not 'image', 'video', or 'webcam'
        print("Invalid mode. Please choose 'image', 'video', or 'webcam'.") # print the message