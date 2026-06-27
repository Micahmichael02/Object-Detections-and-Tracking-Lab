# No Helmet Detection

## Project Overview
This project detects whether a person is wearing a helmet using YOLO object detection and OCR for number plate recognition. It processes video footage, detects violations, and saves extracted data (number plates and timestamps) in an Excel file.

## Project Structure
- `main.py` - The core script that runs the YOLO model for helmet detection and processes video frames.
- `final.mp4` - Sample video file used for helmet detection.
- `best.pt` - The trained YOLO model for helmet detection.
- `images/` - Directory containing cropped images of detected number plates.
- `data.csv` - CSV file storing extracted data from detections.
- `requirements.txt` - Dependencies required to run the project.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/no-helmet-detection.git
   cd no-helmet-detection
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Ensure `best.pt` (YOLO model) and `final.mp4` (video file) are available.
2. Run the script:
   ```sh
   python main.py
   ```
3. The script will:
   - Detect helmets and number plates.
   - Perform OCR on number plates.
   - Save detected information to an Excel file.
   - Store cropped images of number plates in the corresponding date folder.

## Dependencies
Install the following dependencies via `requirements.txt`:
```
paddlepaddle
opencv-python
numpy
ultralytics
datetime
xlwings
paddleocr
```
 
## Output
- Detected number plates saved as images.
- Extracted text data saved in an Excel file.
- Video frames displayed with detection bounding boxes.

## License
This project is for educational purposes. Modify and use it as needed.

