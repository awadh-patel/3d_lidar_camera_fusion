# Concept, Design, and Implementation of Real-Time Camera-LiDAR Fusion for 3D Object Detection and Depth Estimation

This repository contains the implementation of my master's thesis. It demonstrates the integration of a ZED 2i stereo camera and Ouster OS0-128 LiDAR within a ROS2 Humble on Ubuntu 22.04 based framework, enabling real-time 3D object detection and depth estimation. It supports both **Software-in-the-Loop (SiL)** using Gazebo and **Hardware-in-the-Loop (HiL)** with real sensors.

## Workspaces
- **ouster_ws**: Operates the LiDAR and visualizes point clouds in RViz2 
- **zed_ws**: Operates the ZED camera and its functions - **depth_ws**: 
Fuses ZED and LiDAR data for object detection and depth estimation - 
**gazebo_ws**: Software-in-the-Loop (SiL) simulation with robot in urban 
environment - **yolobot**: YOLOv8 object detection code for simulation

## Documentation
- Thesis report is available in the `docs/` folder.

---

## 🗂️ Workspaces & Folders

### `ouster_ws/`
- ROS2 workspace for the Ouster OS-0 LiDAR
- Configures LiDAR point cloud visualization in RViz2
- Based on official Ouster ROS2 drivers

### `zed_ws/`
- ROS2 workspace for ZED 2i stereo camera
- Includes pre-trained ZED object detection
- Publishes RGB, depth, and point cloud streams

### `depth_ws/`
- Integrates ZED object detection with LiDAR depth estimation
- Fuses bounding box coordinates from the camera with point cloud data
- Outputs accurate 3D localization of detected objects

### `gazebo_ws/`
- Software-in-the-Loop simulation using Gazebo and ROS2
- Custom-built 4WD robot with simulated ZED2i and LiDAR
- Launches full robot + sensor stack in an urban simulation world

### `yolobot/`
- YOLOv8-based object detection in simulation
- ROS2 node to detect objects in Gazebo using pre-trained models

---

## 🧪 Features

- ✅ Real-time object detection using YOLOv8 in Gazebo
- ✅ Point cloud generation from LiDAR and stereo camera
- ✅ Accurate depth estimation from Lidar of detected objects by camera
- ✅ Simulated and real-world testing environments
- ✅ ROS2 Humble, RViz2, Gazebo integration

---

## 🚀 Getting Started

```bash
# Clone the repository
https://github.com/awadh-patel/3d_lidar_camera_fusion.git
3d_lidar_camera_fusion

# Build each workspace
cd ouster_ws && colcon build
cd ../zed_ws && colcon build
cd ../depth_ws && colcon build
cd ../gazebo_ws && colcon build



camera_lidar_fusion_thesis/
│
├── README.md
├── LICENSE
├── ouster_ws/             # Workspace for LiDAR
├── zed_ws/                # Workspace for ZED camera
├── depth_ws/              # Object detection and depth estimation
├── gazebo_ws/             # SIL simulation setup
├── yolobot/               # YOLO object detection for Gazebo
└── docs/                  # Optional: thesis PDF, images, diagrams
