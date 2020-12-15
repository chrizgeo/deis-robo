#! usr/bin/env/python3

# Simple navigator for the robot. 
# sends cmd_vel to the teleop_cmd node 
# Christo George
# christogeorge@live.in
# Dec 2020

import time

#ROS2 imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

# A Twist message contains the velocities in meters/sec, angular velocities in rad/sec

class Navigator(Node):

    def __init__(self):
        super().__init__('navigator')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.user_cmd_sub = self.create_subscription(String, 'user_angle', self.user_cmd_cb, 10)
        self.timer = self.create_timer(.01, self.send_velocity)
        self.get_logger().info("Init done")
        self.vel_cmd = Twist()
        self.vel_cmd.linear.x = 0.0
        self.vel_cmd.angular.z = 0.0
    
    def user_cmd_cb(self, msg):
        self.get_logger().info('Got user command angle : "%s" ' % msg.data)
        if('' != msg.data):
            turn_angle = float(msg.data)
            self.turn_angle(turn_angle)

    def send_velocity(self):
        self.publisher_.publish(self.vel_cmd)
        # What is the purpose of this if statement?
        if(self.vel_cmd.linear.x != 0.0 or self.vel_cmd.angular.z != 0.0):
            self.get_logger().info("sent vel cmd")

    def turn_angle(self, angle):
        turningTime = ((1000.0* angle)/180.0)/1000  
        print(turningTime)
        old_x = self.vel_cmd.linear.x
        old_z = self.vel_cmd.angular.z
        self.vel_cmd.linear.x = 100.0 # You are sending a speed of 100 meters/sec !
        self.vel_cmd.angular.z = angle # You are sending degrees, this should be rads
        time.sleep(turningTime)
        self.vel_cmd.linear.x = old_x
        self.vel_cmd.angular.z = old_z


def main(args=None):
    rclpy.init(args=args)
    navigator_ = Navigator()
    rclpy.spin(navigator_)

    navigator_.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
