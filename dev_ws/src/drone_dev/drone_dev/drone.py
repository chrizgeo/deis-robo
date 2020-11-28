# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:03:30 2020

@author: Meerashine Joe
@ Christo George christogeorge@live.in
"""


import rclpy
import threading
import cv2
import time
from rclpy.node import Node
from drone_dev.tello import Tello
from std_msgs.msg import String
from drone_dev.tracker_aruco import arucoTracker
from PIL import Image
import datetime



class droneActor(Node):

    def __init__(self):
        super().__init__('drone_actor')
        self.subscription = self.create_subscription(String, 'DRONE_ACTIONS', self.drone_actor_callback, 10)
        self.subscription  # prevent unused variable warning
        self.timer = self.create_timer(20, self.check_drone_battery)
        self.drone = Tello('', 8889)
        # for streaming
        self.frame = None
        # for aruco detection
        self.aruco_tracker = arucoTracker()
        self.aruco_frame = None
        self.detected_ids = {}

        #always streaming
        self.stream_state = True
        
        # set the drone to command mode
        res = self.drone.send_command('command')
        #res = self.drone.send_command('wifi GROUP1-DRONE verygood')
        self.get_logger().info("Init done")

        #start the stream window
        self.stream_on()

    def __del__(self):
        if(self.stream_state == True):
            self.stream_off()

    #callback for messages received on the drone teleop channel
    def drone_actor_callback(self, msg):
        self.get_logger().info('Got command: "%s"' % msg.data)
        if('' != msg.data):
            self.drone.send_command(msg.data)
    
    #check battery and land if battery is less than 10 percentage
    def check_drone_battery(self):
        battery_level = self.drone.get_battery()
        self.get_logger().info("Battery level %s" % battery_level)
        if(battery_level == 'none_response' or battery_level == 'ok' or battery_level == 'error'):
            return
        if(int(battery_level) < 10):
            self.get_logger().error("Low battery landing")
            self.drone.send_command('land')
    
    #this video veiwing thread runs for the entire time the node is running
    def video_view_thread(self):
        self.get_logger().info("Opencv video thread started")
        
        # wait till we get a valid frame from the drone camera
        while(self.drone.read() is None):
            print("Waiting for video input")
            time.sleep(1)
        self.get_logger().info("Got valid frame, open window now")

        #open the window for the video stream    
        stream_window = "Video stream"
        cv2.namedWindow(stream_window)
        
        #write the video data to a file
        """ now=datetime.datetime.now()
        fileEnd = "%d-%d-%d_%d-%d-%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        videofile = "video/%s.avi" % fileEnd
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        video_ = cv2.VideoWriter(videofile, fourcc, 20.0, (960, 720)) """
        
        # Runs while 'stream_state' is True
        # the stream_state boolean is used to keep the thread alive
        while self.stream_state:
                
                # read the frame from the drone camera
                self.frame = self.drone.read()
                if self.frame is None or self.frame.size == 0:
                    continue 
                # transfer the format from frame to image         
                #image = Image.fromarray(self.frame)
                #cv2.imshow(stream_window, self.frame)
                self.aruco_frame , self.detected_ids = self.aruco_tracker.track_aruco(self.frame)
                cv2.imshow(stream_window, self.aruco_frame)
                #write video to file
                """ video_.write(self.frame) """

                # Video Stream is closed if escape key is pressed
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
        cv2.destroyWindow(stream_window)
        #release the video file
        """ video_.release() """

    #start the video viewing thread to display the current video
    def stream_on(self):
        self.stream_state = True
        self.video_thread = threading.Thread(target=self.video_view_thread)
        self.video_thread.daemon = True
        self.video_thread.start()
   
    #stop the video viewing thread
    def stream_off(self):
        self.stream_state = False
        self.video_thread.stop()

def main(args=None):
    rclpy.init(args=args)
    drone_ = droneActor()
    rclpy.spin(drone_)

    drone_.destroy_node()
    rclpy.shutdown()
    
    
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
    

if __name__ == '__main__':
    main()

   