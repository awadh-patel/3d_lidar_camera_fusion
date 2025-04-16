import rclpy
from rclpy.node import Node
from zed_interfaces.msg import ObjectsStamped  # Assuming this is the message type for object detection

class ObjectDetectionListener(Node):
    def __init__(self):
        super().__init__('object_detection_listener')
        self.subscription = self.create_subscription(
            ObjectsStamped,
            '/zed/zed_node/obj_det/objects',  # Replace with your actual topic
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        for obj in msg.objects:
            # Extract the bounding box and class label
            bbox = obj.bounding_box_2d
            class_label = obj.label

            # Print or process the bounding box and class label
            self.get_logger().info(f'Object: {class_label}')
            self.get_logger().info(f'Bounding Box: {bbox.corners}')

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
