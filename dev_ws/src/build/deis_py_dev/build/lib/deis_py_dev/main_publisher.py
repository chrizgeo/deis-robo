import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class MainNode(Node):
        def __init__(self):
            super().__init__('main_publisher')
            self.publisher_ = self.create_publisher(String, 'DIPLOMA', 10)
            timer_period = 3
            self.timer = self.create_timer(timer_period, self.timer_callback)
            self.i = 0
        
        def timer_callback(self):
            msg = String()
            msg.data = '%d %d' %(self.i, -self.i)
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing wheel speeds "%s"' %msg.data)
            self.i += 10

def main(args=None):
        rclpy.init(args=args)
        main_publisher = MainNode()
        rclpy.spin(main_publisher)

        #destroy is optional
        main_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
