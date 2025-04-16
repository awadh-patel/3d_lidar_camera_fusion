#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from zed_interfaces.msg import ObjectsStamped
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
import numpy as np

class ObjectDetectionListener(Node):
    def __init__(self):
        super().__init__('object_detection_listener')

        # Subscribe to object detection topic
        self.subscription = self.create_subscription(
            ObjectsStamped,
            '/zed/zed_node/obj_det/objects',  # Replace with your actual topic
            self.listener_callback,
            10)

        # Define QoS settings
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=5,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )

        # Subscribe to LiDAR point cloud topic with specified QoS
        self.point_cloud_sub = self.create_subscription(
            PointCloud2,
            '/ouster/points',  # Replace with your actual LiDAR point cloud topic
            self.point_cloud_callback,
            qos_profile)

        self.latest_point_cloud = None

    def point_cloud_callback(self, msg):
        self.latest_point_cloud = msg
        self.get_logger().info(f'Received point cloud with {msg.width * msg.height} points')  # helps confirm that the point cloud data is being received


    def listener_callback(self, msg):
        if self.latest_point_cloud is None:
            self.get_logger().info("No point cloud data received yet.")
            return
        
        for obj in msg.objects:
            bbox = obj.bounding_box_2d
            class_label = obj.label
            self.get_logger().info(f'Object: {class_label}')
            self.get_logger().info(f'Bounding Box: {bbox.corners}')

            # Extract points within the bounding box from the point cloud
            points = self.extract_points_within_bbox(bbox, self.latest_point_cloud)
            if points.size == 0:
                self.get_logger().info(f'No points found in bounding box for {class_label}')
                continue

            # Compute depth
            depths = np.sqrt(points['x']**2 + points['y']**2 + points['z']**2)     
            avg_depth = np.mean(depths)
            self.get_logger().info(f'Average Depth for {class_label}: {avg_depth:.2f} meters')

    def extract_points_within_bbox(self, bbox, point_cloud):
        # Convert bounding box to 2D pixel coordinates
        bbox_x_min = bbox.corners[0].kp[0]
        bbox_y_min = bbox.corners[0].kp[1]
        bbox_x_max = bbox.corners[2].kp[0]
        bbox_y_max = bbox.corners[2].kp[1]

        # Convert PointCloud2 message to an array of points
        cloud_points = list(pc2.read_points(point_cloud, field_names=("x", "y", "z"), skip_nans=True))

        # Placeholder transformation from image coordinates to LiDAR coordinates (customize as needed)
        def transform_to_image_coordinates(point):
            # Dummy transformation for illustration; actual transformation needed based on camera and LiDAR calibration
            img_x = int(point[0] * 10 + 320)  # Replace with actual transformation
            img_y = int(point[1] * 10 + 240)  # Replace with actual transformation
            return img_x, img_y
        
        # Extract points within the bounding box
        points_within_bbox = []
        for point in cloud_points:
            img_x, img_y = transform_to_image_coordinates(point)
            if bbox_x_min <= img_x <= bbox_x_max and bbox_y_min <= img_y <= bbox_y_max:
                points_within_bbox.append(point)

        return np.array(points_within_bbox)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
