#!python3
# Ioannis Broumas
# ioabro17@student.hh.se
# Christo George
# christogeorge@live.in
# Nov 2020

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class GPSNode(Node):
        def __init__(self):
            super().__init__('gps_node')
            self.gps_subscription = self.create_subscription(String, '/robotPositions', self.gps_callback, 10 )
            #self.publisher_ = self.create_publisher(String, 'Group1', 10)
            
        def gps_callback(self,msg):
            self.get_logger().info('Publishing')
            self.get_logger().info('Publishing: "%s"' %msg.data)
            

def main(args=None):
        rclpy.init(args=args)
        g = GPSNode()
        #msg = String()
        #msg.data = 'Hello from Group1!'
        #g.publisher_.publish(msg)
        rclpy.spin(g)

        #destroy is optional
        g.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
