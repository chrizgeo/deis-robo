#! /bin/python3

# Ioannis Broumas
# ioabro17@student.hh.se
# Christo George
# christogeorge@live.in
# Meerashine Joe
# meerashine1995@gmail.com
# Nov 2020

import rclpy
from rclpy.node import Node
import serial
import datetime

from std_msgs.msg import String

class SparkieNode(Node):

    def __init__(self):
        super().__init__('sparkie_subscriber')
        self.subscription = self.create_subscription(String, 'WHEEL_SPEEDS', self.wheelspeed_callback, 10 ) # Don't change this
        self.publisher_odom = self.create_publisher(String, 'odom_raw', 10)
        self.publisher_imu = self.create_publisher(String, 'imu_r', 10)
        timer_period = 0.1 # seconds
        self.timer = self.create_timer(.01, self.get_sensorData_callback)
        self.ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
        self.sensor_readings_file = open("data/sensor-readings.csv", "w")
        self.old_msg = String()
        self.old_msg.data = '0 0'
        self.get_logger().info('Node init finished')

    def wheelspeed_callback(self, msg):
        #self.get_logger().info('old wheel speeds : "%s"' %self.old_msg.data)
        #self.get_logger().info('new wheel speeds : "%s"' %msg.data)
        #if(self.old_msg.data != msg.data):
        self.ser.flush()        
        self.get_logger().info('Got wheel speeds : "%s"' %msg.data)
        self.ser.write(msg.data.encode())
        self.old_msg.data = msg.data
        
    def get_sensorData_callback(self):
    	if(self.ser.in_waiting > 0):
    		data = self.ser.readline().decode()
    		#self.sensor_readings_file.write('{}, {}'.format(datetime.datetime.now().strftime('%H:%M:%S.%f'), data))
    		#self.sensor_readings_file.write(data)
    		msg = String()
    		msg.data = data
    		#data = data.split(sep=" ")
    		#encoders_raw = data[0].split(sep="_")
    		#lin_acc_raw = data[1].split(sep="_")
    		#ang_raw = data[2].split(sep="_")
    		self.publisher_odom.publish(msg)
    		#self.publisher_imu(data)


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

