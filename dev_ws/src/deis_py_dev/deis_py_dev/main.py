#! /bin/python3

# Ioannis Broumas
# ioabro17@student.hh.se
# Christo George
# christogeorge@live.in
# Nov 2020

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class MainNode(Node):
        def __init__(self):
            super().__init__('main_node')
            self.publisher_ = self.create_publisher(String, 'WHEEL_SPEEDS', 10)
            self.teleop_subscription = self.create_subscription(String, 'TELEOP', self.teleop_callback, 10 )
            self.teleop_subscription  # prevent unused variable warning
            #timer_period = 3
            #self.timer = self.create_timer(timer_period, self.teleop_callback)
            #self.i = 0
            self.get_logger().info('Node Main initialized!')
            
        ''' def timer_callback(self):
            msg = String()
            msg.data = '%d %d' %(self.i, -self.i)
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing wheel speeds "%s"' %msg.data)
            self.i += 10 '''
            
        def teleop_callback(self,msg):
            msg.data = msg.data + '\n'
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing wheel speeds "%s"' %msg.data)
            #self.i += 10
            

def main(args=None):
        rclpy.init(args=args)
        main_node = MainNode()
        rclpy.spin(main_node)

        #destroy is optional
        main_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
