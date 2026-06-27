
# Color Detection Project

## Overview

This project consists of two main scripts: `util.py` and `color_detection.py`. These scripts work together to detect and highlight specific colors in live video streams.

## Files Explained

### util.py

The `util.py` script defines a utility function `get_limits` that calculates the HSV (Hue, Saturation, Value) color range for a given BGR (Blue, Green, Red) color. This range is crucial for detecting specific colors in an image or video.

#### Key Features:
- **Importing Required Libraries**: Utilizes `numpy` for array manipulation and `cv2` (OpenCV) for image processing.
- **Converting BGR to HSV**: Converts a BGR color to HSV using OpenCV's `cv2.cvtColor` function, as HSV is better suited for color segmentation.
- **Extracting the Hue Value**: Extracts the hue value (the first channel) from the HSV color, representing the color type (e.g., red, green, blue).
- **Handling Red Hue Wrap-around**: Manages special cases for red hue wrap-around in the HSV scale:
  - If the hue is at the higher end (>=165), sets the upper limit to the maximum value (180) and adjusts the lower limit accordingly.
  - If the hue is at the lower end (<=15), sets the lower limit to 0 and adjusts the upper limit.
  - For other hues, calculates the range normally.
- **Returning Limits**: Returns the lower and upper HSV limits for the input BGR color, which can be used for color segmentation.

### color_detection.py

The `color_detection.py` script captures live video from the webcam, detects a specific color (yellow), and highlights it with a bounding box in the video stream.

#### Key Features:
- **Importing Libraries**: Uses OpenCV for video and image processing, PIL (Python Imaging Library) for image manipulation, and the `get_limits` function from `util.py` to compute HSV color ranges.
- **Defining the Target Color**: Defines the target color in BGR format as `yellow = [0, 255, 255]`.
- **Setting Up the Video Stream**: Initializes a video stream using OpenCV's `VideoCapture` function to access the default webcam.
- **Processing Each Frame**:
  - Captures frames from the webcam.
  - Converts each frame to the HSV color space for easier color detection.
  - Calculates the HSV limits for yellow using the `get_limits` function.
- **Creating a Mask**: Generates a binary mask to highlight pixels within the yellow color range (white) and others as black.
- **Finding the Bounding Box**:
  - Converts the binary mask into a PIL image to use the `getbbox` method for finding the bounding box around white regions.
  - If a bounding box is found, extracts its coordinates and draws a green rectangle on the original frame to highlight the detected area.
- **Displaying the Result**: Shows the mask (highlighting the detected areas) in a window using OpenCV's `imshow`.
- **Exiting the Loop**: Continues the loop until the user presses the 'q' key. The video stream is then released, and all OpenCV windows are closed.

## Usage Instructions

1. **Install Dependencies**:
   ```bash
   pip install numpy opencv-python pillow
   ```

2. **Run the Color Detection Script**:
   ```bash
   python color_detection.py
   ```

3. **Interact with the Video Stream**:
   - The script will open a window showing the live video stream with detected yellow areas highlighted by bounding boxes.
   - Press 'q' to exit the video stream.

## Contributing

Feel free to fork this project, make improvements, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For any questions or inquiries, please contact the project maintainer at [makoflash05@gmail.com].

---

