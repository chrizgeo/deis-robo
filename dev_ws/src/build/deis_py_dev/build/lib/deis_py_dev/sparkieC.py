import rclpy
from rclpy.node import Node
import serial

from std_msgs.msg import String

class SparkieNode(Node):

    def __init__(self):
        super().__init__('sparkie_subscriber')
        self.subscription = self.create_subscription(String, 'teleop', self.listener_callback, 10 )
        self.subscription #prevent unused variable warning
        self.ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)

    def listener_callback(self, msg):
        self.get_logger().info('Got wheel speeds : "%s"' %msg.data)
        self.ser.write(msg.data.encode(encoding='UTF-8'))

def main(args=None):
    rclpy.init(args=args)
    sparkie_node = SparkieNode()
    sparkie_node.ser.flush()
    rclpy.spin(sparkie_node)

    sparkie_node.destroy_node()

    rclpy.shutdown()
    

if __name__ == '__main__':
    main()

