import rclpy
from rclpy.node import Node

from sensor_msgs.msg import NavSatFix


class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection')
        self.gps_in_subs = self.create_subscription(
            NavSatFix,
            '/mavros/global_position/global',
            self.gps_callback,
            rclpy.qos.QoSPresetProfiles.SENSOR_DATA.value
        )
        self.gps_in_subs
        self.__longitude = 0
        self.__latitude = 0
        self.__altitude = 0

    def gps_callback(self, msg):
        # Process GPS data
        # ...
        self.__longitude = msg.longitude
        self.__latitude = msg.latitude
        self.__altitude = msg.altitude
        self.get_logger().info(f'Longitude {msg.longitude}, Latitude {msg.latitude}, Altitude {msg.altitude}')

    def retrieve_gps_data(self):
        return self.__longitude, self.__latitude, self.__altitude


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
