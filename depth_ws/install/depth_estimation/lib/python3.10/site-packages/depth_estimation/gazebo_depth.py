#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String, Float64
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2

class DepthEstimationNode(Node):

    def __init__(self):
        super().__init__('depth_estimation_node')
        
        # Subscriber to YOLOv8 object detection results
        self.yolo_subscription = self.create_subscription(
            String,
            '/inference_result',
            self.yolo_detection_callback,
            10)

        # Subscriber to LiDAR point cloud
        self.lidar_subscription = self.create_subscription(
            PointCloud2,
            '/scan',
            self.lidar_callback,
            10)

        # Publisher for depth estimation results
        self.depth_publisher = self.create_publisher(
            Float64,
            '/depth_estimation',
            10)

        # Buffer for storing LiDAR data
        self.lidar_data = None

    def yolo_detection_callback(self, msg):
        # Process YOLOv8 object detection results here
        detections = msg.data.split(';')  # Example: parse msg.data into detections

        for detection in detections:
            # Estimate depth using LiDAR data
            depth = self.estimate_depth_from_lidar(detection)
            # Publish depth estimation result
            depth_msg = Float64()
            depth_msg.data = depth
            self.depth_publisher.publish(depth_msg)

    def lidar_callback(self, msg):
        # Store LiDAR point cloud data for use in depth estimation
        self.lidar_data = msg

    def estimate_depth_from_lidar(self, detection):
        if self.lidar_data is None:
            return float('nan')  # No LiDAR data available

        # Parse detection to get the bounding box or region of interest
        # For simplicity, assume detection format is "class xmin ymin xmax ymax"
        detection_parts = detection.split()
        if len(detection_parts) != 5:
            return float('nan')

        object_class, xmin, ymin, xmax, ymax = detection_parts
        xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])

        # Convert PointCloud2 data to numpy array
        point_cloud = np.array(list(pc2.read_points(self.lidar_data, skip_nans=True)))

        # Filter points within the bounding box
        # Assuming the camera and LiDAR are perfectly aligned and the bounding box is in pixel coordinates
        # This is a simplification. In practice, you would need to transform points to the camera frame and project them.
        points_in_bbox = [point for point in point_cloud if xmin <= point[0] <= xmax and ymin <= point[1] <= ymax]

        if not points_in_bbox:
            return float('nan')  # No points found in the bounding box

        # Estimate depth as the average distance of points in the bounding box
        depths = [point[2] for point in points_in_bbox]  # Assuming Z is the depth
        average_depth = np.mean(depths)

        return average_depth

def main(args=None):
    rclpy.init(args=args)
    node = DepthEstimationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
