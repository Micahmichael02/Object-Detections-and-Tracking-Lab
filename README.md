# CV- Object Detection, Face Attendance, Gesture Recognition, Depth Estimation, ROI-based Analytics Projects

A portfolio of standalone computer vision projects — object detection, face attendance/recognition, gesture & sign-language recognition, depth estimation, and ROI-based analytics. Each project lives in its own folder with its own dependencies and is run independently.

## Contents

| # | Project | Category | Folder |
|---|---------|----------|--------|
| 1 | [Engine Part Detection](#1-engine-part-detection) | Object Detection (VLM) | `Engine Part Detection/` |
| 2 | [Face Attendance — Face Recognition](#2-face-attendance--face-recognition) | Face Attendance | `Face-attendance-Face-recognition/` |
| 3 | [Smart Attendance with Real-Time Database](#3-smart-attendance-with-real-time-database) | Face Attendance | `Smart-Attendance-with-Real-Time-Database/` |
| 4 | [No Helmet Detection](#4-no-helmet-detection) | Object Detection + OCR | `no_helmet_detection/` |
| 5 | [OD ROI Areas](#5-od-roi-areas) | Object Detection + Tracking | `OD_ROI_Areas/` |
| 6 | [Sign Language Detection](#6-sign-language-detection) | Gesture Recognition | `sign_lan_detections/` |
| 7 | [Monocular Depth + 3D Object Detection](#7-monocular-depth--3d-object-detection) | Object Detection + Depth | `monocular-depth-object-detection-main/` |
| 8 | [Computer Vision Based Track Pad](#8-computer-vision-based-track-pad-airscroll) | Gesture Recognition | `Computer-Vision-Based-Track-Pad-main/` |
| 9+ | _Reserved for future projects_ | — | — |

Jump to [Converting an MP4 result into a GIF](#converting-an-mp4-result-into-a-gif) and [Adding more projects](#adding-more-projects).

---

## 1. Engine Part Detection

Identifies engine parts in a video stream by sending sampled frames to Google's Gemini vision model and printing back the part name and material.

- **Script:** `Enginepart.py`
- **Input:** `parts.mp4` (a Mega.nz download link for the sample clip is in `vid.txt`), or a webcam (pass an empty string).
- **Model:** `gemini-2.0-flash` via `langchain-google-genai` (cloud inference, no local weights).

### Run it
```bash
cd "Engine Part Detection"
pip install opencv-python langchain-core langchain-google-genai
# set your own key instead of the one hardcoded in Enginepart.py
set GOOGLE_API_KEY=your-key-here        # PowerShell: $env:GOOGLE_API_KEY="your-key-here"
python Enginepart.py
```
Press `q` to stop. Every 5 seconds the current frame is sent to Gemini and the identified part/material is printed to the console — that console output is the "result" for this project (no file is written).

> ⚠️ `Enginepart.py` currently hardcodes a Google API key as a fallback default. Replace it with your own key and avoid committing real keys to source control.

---

## 2. Face Attendance — Face Recognition

A Tkinter desktop app that logs in/out users by webcam face recognition (via `face_recognition`/`dlib` embeddings) and stores a timestamped attendance log.

- **Scripts:** `main.py` (basic, single-face, `.txt` log) and `Main_Updated.py` (multi-face, adds a `.csv` log).
- **Database:** `db/` holds one `.pickle` (face embedding) + `.png` (captured photo) per registered user.

### Run it
```bash
cd Face-attendance-Face-recognition
pip install -r requirements.txt
python Main_Updated.py     # or: python main.py
```
1. Click **register new user**, capture a face, and name it.
2. Click **Login** / **logout** to recognize the face against `db/` and append a row to `log.txt` / `log.csv`.

**Results / analysis:** `log.csv` (Name, Date, Timestamp, Action) and `log.txt` are the attendance records to analyze.

**Sample registered user** (`db/Michael Micah.png`):

<img src="Face-attendance-Face-recognition/db/Michael%20Micah.png" alt="Registered user sample" width="260"/>

---

## 3. Smart Attendance with Real-Time Database

A Firebase-backed attendance kiosk: recognizes a face, looks up the student in Firebase Realtime Database/Storage, and increments their attendance counter with a styled overlay UI.

- **Scripts (run in order):** `AddDatatoDatabase.py` → `EncodeGenerator.py` → `main.py`.

### Run it
```bash
cd Smart-Attendance-with-Real-Time-Database
pip install opencv-python face_recognition cvzone numpy firebase_admin
```
1. Add your Firebase service account file as `serviceAccountKey.json` and fill in `databaseURL`/`storageBucket` in `main.py`.
2. Provide `Resources/background.png` and `Resources/Modes/*.png` (UI background/overlay assets — not included in this checkout) plus student photos uploaded to Firebase Storage under `Images/<id>.png`.
3. `python AddDatatoDatabase.py` — seed student records into Firebase.
4. `python EncodeGenerator.py` — builds `EncodeFile.p` (face encodings) from the student photos.
5. `python main.py` — runs the live webcam attendance kiosk.

**Results / analysis:** attendance counts and `last_attendance_time` are updated directly in the Firebase Realtime Database (`Students/<id>`), viewable from the Firebase console.

> This folder ships only the source scripts — the `Resources/` UI assets, `serviceAccountKey.json`, and `EncodeFile.p` are generated/provided locally and intentionally not committed.

---

## 4. No Helmet Detection

YOLO detects riders without a helmet plus their number plate inside a defined ROI polygon; PaddleOCR reads the plate text and logs the violation.

- **Script:** `main.py`
- **Model:** `best.pt` (custom YOLO)
- **Input:** `final.mp4`

### Run it
```bash
cd no_helmet_detection
pip install -r requirements.txt
python main.py
```
Press `q` to stop.

**Results / analysis:** for each violation, a cropped plate image is saved into a folder named for today's date (e.g. `2025-01-06/`) as `<plate-text>_<HH-MM-SS>.jpg`, and a row `[Number Plate, Date, Time]` is appended to `<date>/<date>.xlsx` for downstream analysis.

**Sample detected plate crops** (`2025-01-06/`):

<p>
  <img src="no_helmet_detection/2025-01-06/KL.07BU.5S01_22-28-58.jpg" alt="Detected plate crop 1" height="110"/>
  <img src="no_helmet_detection/2025-01-06/KL38F1391_22-48-58.jpg" alt="Detected plate crop 2" height="110"/>
</p>

---

## 5. OD ROI Areas

Counts/labels people inside a hand-defined ROI polygon using YOLO11 + tracking, and writes an annotated output video.

- **Script:** `main.py`
- **Model:** `yolo11s.pt`
- **Input:** `pcount.mp4`, **Output:** `output.mp4`

### Run it
```bash
cd OD_ROI_Areas
pip install opencv-python numpy ultralytics cvzone
python main.py
```
Press `q` to stop early.

**Results / analysis:** `output.mp4` — the annotated video with the ROI polygon and labeled detections inside it, ready for review.

**Result preview** (`output.gif`, generated from `output.mp4`):

![OD ROI Areas demo](OD_ROI_Areas/output.gif)

---

## 6. Sign Language Detection

Classifies static hand signs (A/B/L) from MediaPipe hand landmarks using a trained scikit-learn classifier, and records the annotated webcam feed.

- **Pipeline:** `data_collections.py` (capture samples) → `create_dataset.py` (extract landmark features → `data.pkl`) → `train_classifier.py` (train + evaluate → `model.p`, training plots) → `test_classifier.py` (live inference → `output.mp4`).

### Run it
```bash
cd sign_lan_detections
pip install -r requirements.txt
python test_classifier.py     # live inference using the pretrained model.p
```
To retrain from scratch: `python data_collections.py` → `python create_dataset.py` → `python train_classifier.py`.

**Results / analysis:** `train_classifier.py` reports accuracy and saves evaluation plots (`Figure_1.png`, `Figure_2.png`, `Figure_3.png`); `test_classifier.py` writes the live-annotated session to `output.mp4`.

**Training result plots:**

<p>
  <img src="sign_lan_detections/Figure_1.png" alt="Sign language training Figure 1" width="260"/>
  <img src="sign_lan_detections/Figure_2.png" alt="Sign language training Figure 2" width="260"/>
  <img src="sign_lan_detections/Figure_3.png" alt="Sign language training Figure 3" width="260"/>
</p>

**Live inference preview** (`output.gif`, generated from `output.mp4`):

![Sign language detection demo](sign_lan_detections/output.gif)

---

## 7. Monocular Depth + 3D Object Detection

YOLO detection/segmentation combined with monocular depth estimation (Apple ml-depth-pro) and Open3D to produce per-object distances and 3D bounding boxes. See its own [README](monocular-depth-object-detection-main/README.md) and [PROJECT_GUIDE.md](monocular-depth-object-detection-main/PROJECT_GUIDE.md) for full pipeline details.

### Run it
```bash
cd monocular-depth-object-detection-main
pip install -r requirements.txt
python distance_estimation_yolo_video.py     # 2D boxes annotated with distance
python seg_3d_bbox_video.py                  # 3D point clouds + 3D bounding boxes
```

**Results / analysis:** annotated frames with distance labels, depth-map visualizations, and rendered 3D point clouds/bounding boxes.

**Example output:**

<img src="monocular-depth-object-detection-main/examples/frame_0027.jpg" alt="Monocular depth example" width="500"/>

---

## 8. Computer Vision Based Track Pad (AirScroll)

Touchless scroll control: a YOLOv5 classifier detects an "Active"/"Inactive" hand state and optical flow translates hand motion into scroll events, with a HUD overlay.

- **Script:** `main.py`
- **Model:** `best.pt` (YOLOv5 classification)

### Run it
This script imports directly from a local `yolov5` checkout (`models.common`, `utils.general`, `utils.torch_utils`), so it must sit two directories below a cloned [ultralytics/yolov5](https://github.com/ultralytics/yolov5) repo (or adjust `YOLO_ROOT` in `main.py`).
```bash
git clone https://github.com/ultralytics/yolov5
pip install opencv-python torch torchvision pyautogui numpy
# place/copy Computer-Vision-Based-Track-Pad-main two levels under yolov5/, then:
cd Computer-Vision-Based-Track-Pad-main
# edit MODEL_PATH in main.py to point at best.pt
python main.py
```
Press `q` to stop.

**Results / analysis:** a live HUD shows classification confidence, scroll speed, FPS, and optical-flow direction arrows — see the [project README](Computer-Vision-Based-Track-Pad-main/README.md) for a recorded demo clip.

---

## Converting an MP4 result into a GIF

Every project above that writes an `output.mp4`/result video can be turned into a lightweight, README-friendly GIF the same way (uses `ffmpeg`'s two-pass palette generation for good quality at a small file size):

```bash
ffmpeg -y -i input.mp4 -t 8 -vf "fps=8,scale=400:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```
- `-t 8` — only encode the first 8 seconds (drop it to convert the whole clip).
- `fps=8` — lower frame rate keeps the GIF small.
- `scale=400:-1` — resize width to 400px, keep aspect ratio (raise/lower for quality vs. size).

This is exactly the command used to generate `OD_ROI_Areas/output.gif` and `sign_lan_detections/output.gif` above.

---

## Adding more projects

This README is structured so a new project just needs a new numbered section following the same template:

```markdown
## N. <Project Name>

Short description of what it does.

- **Script:** ...
- **Model/Input:** ...

### Run it
\`\`\`bash
cd <folder>
pip install -r requirements.txt
python <script>.py
\`\`\`

**Results / analysis:** where output files/images/video land and what to look at.

<!-- embed any output images/GIFs here -->
```

Add the new row to the [Contents](#contents) table at the top, pointing at the new section anchor and folder.
