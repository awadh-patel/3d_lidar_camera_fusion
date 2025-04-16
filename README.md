# Real-Time Camera and LiDAR Fusion for 3D Object Detection and Depth 
# Estimation

This repository contains the implementation of my master's thesis. It 
demonstrates the integration of a ZED 2i stereo camera and Ouster 
OS0-128 LiDAR within a ROS2-based framework, enabling real-time 3D 
object detection and depth estimation.

## Workspaces
- **ouster_ws**: Operates the LiDAR and visualizes point clouds in RViz2 
- **zed_ws**: Operates the ZED camera and its functions - **depth_ws**: 
Fuses ZED and LiDAR data for object detection and depth estimation - 
**gazebo_ws**: Software-in-the-Loop (SiL) simulation with robot in urban 
environment - **yolobot**: YOLOv8 object detection code for simulation

## Documentation
- Thesis report and presentation are available in the `docs/` folder.

## How to run (to be added)
