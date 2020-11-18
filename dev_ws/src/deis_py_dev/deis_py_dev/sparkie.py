#! usr/bin/env/python3

# Ioannis Broumas
# ioabro17@student.hh.se
# Christo George
# christogeorge@live.in
# Meerashine Joe
# meerashine1995@gmail.com
# Nov 2020

import serial
import datetime

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class SparkieNode(Node):

    def __init__(self):
        super().__init__('sparkie_subscriber')
        self.subscription = self.create_subscription(String, 'WHEEL_SPEEDS', self.wheelspeed_callback, 10 ) # Don't change this
        self.subscription = self.create_subscription(String, 'GPS', self.gps_callback, 10 )
        self.publisher_odom = self.create_publisher(String, 'odom_raw', 20)
        self.publisher_imu = self.create_publisher(String, 'imu_r', 10)
        timer_period = 0.1 # seconds
        self.timer = self.create_timer(timer_period, self.get_sensorData_callback)
        self.ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
        self.sensor_readings_file = open("data/sensor-readings.csv", "w")
        self.old_msg = String()
        self.old_msg.data = '0 0'
        self.get_logger().info('Node Sparkie initialized!')

    def wheelspeed_callback(self, msg):
        self.get_logger().info('Got wheel speeds : "%s"' %msg.data)
        self.ser.write(msg.data.encode())
        self.old_msg.data = msg.data
        
    def gps_callback(self, msg):
        self.ser.write(msg.data.encode())
        
    def get_sensorData_callback(self):
    	if(self.ser.in_waiting > 0):
    		data = self.ser.readline().decode()
    		#self.sensor_readings_file.write(data)
    		data = data.split(sep=" ")
    		current_time = self.get_clock().now().to_msg()
    		msg_imu = String()
    		#msg_imu.data = current_time + "_" + data[0]
    		msg_imu.data = data[0]
    		self.publisher_imu.publish(msg_imu)
    		msg_enc = String()
    		#msg_enc.data = current_time + "_" + data[1]
    		msg_enc.data = data[1]
    		self.publisher_odom.publish(msg_enc)
    		

def main(args=None):
    rclpy.init(args=args)
    sparkie_node = SparkieNode()
    sparkie_node.ser.flush()
    rclpy.spin(sparkie_node)
    sparkie_node.sensor_readings_file.close()
    sparkie_node.destroy_node()
    
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()

