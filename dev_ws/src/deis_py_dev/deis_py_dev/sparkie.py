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
        self.subscription = self.create_subscription(String, 'DIPLOMA', self.wheelspeed_callback, 10 )
        self.subscription #prevent unused variable warning
        self.create_timer(.01, self.get_sensorData_callback)
        self.ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
        self.sensor_readings_file = open("data/sensor-readings.csv", "w")

    def wheelspeed_callback(self, msg):
        self.get_logger().info('Got wheel speeds : "%s"' %msg.data)
        self.ser.write(msg.data.encode(encoding='UTF-8'))
        
    def get_sensorData_callback(self):
    	if(self.ser.in_waiting > 0):
    		data = self.ser.readline().decode()
    		self.sensor_readings_file.write('{}, {}'.format(datetime.datetime.now().strftime('%H:%M:%S.%f'), data))
    		#self.sensor_readings_file.write(data)
    		data = data.split(sep=" ")
    		encoders_raw = data[0].split(sep="_")
    		lin_acc_raw = data[1].split(sep="_")
    		ang_raw = data[2].split(sep="_")


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

