# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 19:40:04 2020

@author: Meerashine Joe
"""

import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import pickle
import os

#the aruco tracker class
class arucoTracker():
    def __init__(self):
        self.calibrate_camera()
        self.mtx = None
        self.dist = None
    
    #calibrate the camera with the provided pckl file
    def calibrate_camera(self):
        # Check for camera calibration data
        if not os.path.exists('./src/drone_dev/drone_dev/calibration2.pckl'):
            print("You need to calibrate the camera you'll be using. See calibration project directory for details.")
            exit()
        else:
            f = open('src/drone_dev/drone_dev/calibration2.pckl', 'rb')
            (ret, self.mtx, self.dist, rvecs, tvecs,) = pickle.load(f)
            f.close()
            if self.mtx is None or self.dist is None:
                print("Calibration issue. Remove ./calibration2.pckl and recalibrate your camera with CalibrateCamera.py.")
                exit()


    #scans the passed frame for aruco markers
    #returns the id and position of the markers if found
    #returns none if no marker was found

    # TODO, add the location of the detected aruco markers also

    def track_aruco(self, frame):
        #a dictionary to store ids detected in the frame, contains id value and position as a tuple
        detected_ids = {}
        # operations on the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # set dictionary size depending on the aruco marker selected
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

        # detector parameters can be set here (List of detection parameters[3])
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10

        # lists of ids and the corners belonging to each id
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
        # font for displaying text (below)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # check if the ids list is not empty
        # if no check is added the code will crash
        if np.all(ids != None):

            # estimate pose of each marker and return the values
            # rvet and tvec-different from camera coefficients
            rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, self.mtx, self.dist)
            (rvec-tvec).any()  # get rid of that nasty numpy value array error

            for i in range(0, ids.size):
                # draw axis for the aruco markers
                aruco.drawAxis(frame, self.mtx, self.dist, rvec[i], tvec[i], 0.1)

            # draw a square around the markers
            aruco.drawDetectedMarkers(frame, corners)
            #print(cv2.norm(tvec), " meters")
            print(cv2.norm(self.dist))

            strg = ''
            for i in range(0, ids.size):
                #TODO change (0,0) to the detected ids position 
                detected_ids[str(ids[i][0])] = (0,0)
                strg += str(ids[i][0])+', '
            #show the detected marker ids on frame
            cv2.putText(frame, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
        
        else:
            # code to show 'No Ids' when no markers are found
            cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

        return frame, detected_ids