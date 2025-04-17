# Concept, Design, and Implementation of Real-Time Camera-LiDAR Fusion for 3D Object Detection and Depth Estimation

This repository contains the implementation of my master's thesis. It demonstrates the integration of a ZED 2i stereo camera and Ouster OS0-128 LiDAR within a ROS2 Humble on Ubuntu 22.04 based framework, enabling real-time 3D object detection and depth estimation. It supports both **Software-in-the-Loop (SiL)** using Gazebo and **Hardware-in-the-Loop (HiL)** with real sensors.

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


🚨️ FOR OUSTER OS 0 LIDAR 🚨️

# to launch lidar
ros2 launch ouster_ros sensor.launch.xml    \
    sensor_hostname:=os-122340001156.local
    
# to start recording data
ros2 launch ouster_ros record.launch.xml    \
    sensor_hostname:=<sensor host name>     \
    bag_file:=<optional bag file name>      \
    metadata:=<json file name>
    
# to play recorded data
ros2 launch ouster_ros replay.launch.xml    \
    bag_file:=<path to rosbag file>         \
    metadata:=<json file name>


📷️ FOR STEREOLABS ZED 2I CAMERA 📷️

# to start node 
ros2 launch zed_wrapper zed_camera.launch.py camera_model:='zed2i'

# to visualize started node in rviz2
ros2 launch zed_display_rviz2 display_zed_cam.launch.py camera_model:=zed2i sim_mode:=true

# to start svo video recording
ros2 service call /zed/zed_node/start_svo_rec zed_interfaces/srv/StartSvoRec 

# to stop svo video recording
ros2 service call /zed/zed_node/stop_svo_rec zed_interfaces/srv/StartSvoRec 

# to start node of svo video recording
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i svo_path:=/home/awadh/zed.svo

# to start and visualize svo video recording with rviz2
ros2 launch zed_display_rviz2 display_zed_cam.launch.py camera_model:=zed2i svo_path:=/home/awadh/zed.svo

# to manually start object detection service 
ros2 service call /zed/zed_node/enable_obj_det std_srvs/srv/SetBool "{'data' : true}"

# to manually stop object detection service
ros2 service call /zed/zed_node/enable_obj_det std_srvs/srv/SetBool "{'data' : false}"

# topic for rviz2 Zed OD Display
/zed/zed_node/obj_det/objects


🌳️ TF 🌳️

# to change the tf
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 zed_camera_link os_sensor
ros2 run tf2_ros static_transform_publisher -0.3 -0.1 0.13 0 0 0 zed_camera_link os_sensor


# to view tf
ros2 run tf2_tools view_frames


📍️ DEPTH ESTIMATION 📍️

# extract object detection results
cd depth_ws/src/depth_estimation/depth_estimation/
./extract_obj.py

# view depth of particular object
cd depth_ws/src/depth_estimation/depth_estimation/
./depth.py

# view depth of all object in frame 
cd depth_ws/src/depth_estimation/depth_estimation/
./depth_info.py
ros2 topic echo /depth_info


🎒️ BAG FILE 🛍️

# to record bag
ros2 bag record -o (name) -a

# to play recorded bag
ros2 bag play -l (name)


		GAZEBO

🤖️ REBOOT GAZEBO 🤖️

# to reboot gazebo
killallgazebo
killallgzclient
killallgzserver


🏎️ Launch Robot 🏎️

ros2 launch my_robot_bringup my_robot_gazebo.launch.xml


🎮️ SIMULATE ROBOT 🕹️

ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 run turtlebot3_teleop teleop_keyboard


🏃️ OBJECT DETECTION IN GAZEBO YOLOv8 🚘️

#  for object detection
cd yolobot/src/yolobot_recognition/scripts
python3 yolov8_ros2_pt.py
# go to rviz and subscribe topic-
/inference_result : Image

# to check the subscriber of object
cd yolobot/src/yolobot_recognition/scripts
python3 yolov8_ros2_subscriber.py
# go to rviz and subscribe topic-
/inference_result_cv2 : Image


🗺️ NAVIGATION IN GAZEBO 🗾️

# for navigation
ros2  launch my_robot_bringup my_robot_gazebo.launch.xml 
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=True map:=maps/my_world.yaml
ros2 run rviz2 rviz2 

3d_lidar_camera_fusion/
│
├── README.md
├── LICENSE
├── ouster_ws/             # Workspace for LiDAR
├── zed_ws/                # Workspace for ZED camera
├── depth_ws/              # Object detection and depth estimation
├── gazebo_ws/             # SIL simulation setup
├── yolobot/               # YOLO object detection for Gazebo
└── docs/                  # Optional: thesis PDF, images, diagrams
