# Monocular Depth Object Detection Project Guide

## Project Overview
This project combines monocular depth estimation with object detection to create a system that can detect objects and estimate their 3D positions from single images. It uses YOLO for object detection and Apple's ml-depth-pro model for depth estimation.

## Project Structure

### Main Files

1. **calibration-camera.py**
   - Purpose: Camera calibration script
   - Function: Calculates camera matrix and distortion coefficients using chessboard patterns
   - Usage: Place chessboard images in 'chessboard_calibration' folder
   - Output: Generates 'CalibrationMatrix_college_cpt.npz' with camera parameters

2. **distance_estimation_yolo.py**
   - Purpose: Single image processing with depth estimation
   - Function: Detects cars and estimates their distance
   - Input: Single image from 'data' folder
   - Output: 
     - Annotated image with bounding boxes and depth values
     - Depth map visualization

3. **distance_estimation_yolo_video.py**
   - Purpose: Process multiple images (video frames)
   - Function: Similar to distance_estimation_yolo.py but for multiple images
   - Input: Images from 'data/car_1' folder
   - Output: 
     - Annotated images with distances
     - Depth maps for each frame

4. **distance_estimation_with_segm_yolo.py**
   - Purpose: Enhanced version with segmentation
   - Function: Detects cars, creates segmentation masks, and estimates depth
   - Input: Single image from 'data' folder
   - Output: 
     - Image with segmentation masks and depth values
     - Depth map visualization

5. **seg_3d_bbox.py**
   - Purpose: 3D bounding box generation
   - Function: Creates 3D point clouds and bounding boxes for detected objects
   - Input: Single image from 'data' folder
   - Output: 
     - 3D point cloud visualization
     - 3D bounding boxes for detected objects

6. **seg_3d_bbox_video.py**
   - Purpose: Process multiple images for 3D reconstruction
   - Function: Similar to seg_3d_bbox.py but for multiple images
   - Input: Images from 'data/car_1' folder
   - Output: 
     - 3D point clouds and bounding boxes for each frame
     - Visualizations saved in 'output/car_1' folder

7. **metric_depth.py**
   - Purpose: Depth map generation and visualization
   - Function: Creates colored point clouds from depth maps
   - Input: Single image from 'data' folder
   - Output: 
     - Point cloud visualization
     - Depth map visualization

8. **metric_depth_test.py**
   - Purpose: Simple depth estimation test
   - Function: Basic depth map generation
   - Input: Single image from 'data' folder
   - Output: Depth map visualization

### Required Folders

1. **data/**
   - Place your test images here
   - For video processing, create subfolders (e.g., 'data/car_1/')
   - Supported formats: .jpg, .png

2. **output/**
   - Created automatically
   - Stores all generated visualizations and results
   - Subfolders:
     - 'car_1/': For video processing results
     - 'car_1_images_with_distance/': Images with distance annotations
     - 'car_1_depth_maps/': Depth map visualizations

3. **chessboard_calibration/**
   - Place chessboard images for camera calibration
   - Required for accurate depth estimation

## Setup and Usage

1. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

2. **Camera Calibration**
   - Place chessboard images in 'chessboard_calibration' folder
   - Run calibration-camera.py
   - This generates camera parameters needed for depth estimation

3. **Testing with Single Images**
   - Place test images in 'data' folder
   - Run any of the single-image scripts:
     - distance_estimation_yolo.py
     - distance_estimation_with_segm_yolo.py
     - seg_3d_bbox.py
     - metric_depth.py

4. **Testing with Multiple Images**
   - Create a folder in 'data' (e.g., 'data/car_1')
   - Place sequence of images in this folder
   - Run either:
     - distance_estimation_yolo_video.py
     - seg_3d_bbox_video.py

## Required Models

1. **YOLO Models**
   - yolo11s.pt: For object detection
   - yolo11s-seg.pt: For segmentation
   - Place these in the project root directory

2. **Depth Model**
   - Uses Apple's ml-depth-pro model
   - Automatically downloaded when running the scripts

## Output Examples

1. **Distance Estimation**
   - Bounding boxes around detected cars
   - Distance values in meters
   - Depth map visualization

2. **3D Reconstruction**
   - Point cloud visualization
   - 3D bounding boxes
   - Depth-based segmentation

## Notes

- Ensure all required models are present
- Camera calibration is crucial for accurate depth estimation
- GPU recommended for faster processing
- Check output folder for results
- Adjust parameters in scripts for different scenarios

## Troubleshooting

1. If depth estimation is inaccurate:
   - Recalibrate camera using calibration-camera.py
   - Check image quality and lighting conditions
   - Verify camera parameters

2. If object detection fails:
   - Ensure YOLO models are properly installed
   - Check image resolution and quality
   - Verify object visibility in images

3. If 3D reconstruction is poor:
   - Check depth map quality
   - Verify camera calibration
   - Ensure sufficient object features for reconstruction 