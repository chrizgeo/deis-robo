# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:03:30 2020

@author: Meerashine Joe
"""


import rclpy
from rclpy.node import Node
from easytello import tello
from std_msgs.msg import String



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Movment happening: "%s"' % msg.data)


def main(args=msg):
    
    my_drone = tello.Tello()
    my_drone.takeoff()
   
    if args == "f":
        my_drone.forward(100)# move the drone forward
    if args =="b":
        my_drone.back(100)# move the drone backward
    if args == "l":
        my_drone.flip_left(100)# move the drone left
    if args == "r":
        my_drone.flip_right(200)# move the drone right
    if args == "S":
        my_drone.forward(100)
        my_drone.spin(100)
        my_drone.land()# the drone will move back and will spin and will stop
    else:
        my_drone.takeoff()
    minimal_subscriber.destroy_node()
    minimal_subscriber.get_logger().info("logging " % args)
    rclpy.shutdown()
    
    
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    

if __name__ == '__main__':
    rclpy.init(args=msg)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    main()

   