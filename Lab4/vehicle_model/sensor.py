import lcm
import select
import numpy as np
import cv2 as cv
import imutils
from exlcm import sensor_message
import time

lc = lcm.LCM()
sensor_message = sensor_message()

global last_timestamp
global curr_timestamp
global isMoving

last_timestamp = curr_timestamp = 0
isMoving = False

def update_sensor_message(shouldBrake):
    print("Publish on SENSOR channel")
    sensor_message.timestamp =  int(time.time()*1000)
    sensor_message.detected_obstacle = shouldBrake
    lc.publish("SENSOR", sensor_message.encode())

cap = cv.VideoCapture(0)
# take first frame of the video
ret,frame = cap.read()
backSub = cv.createBackgroundSubtractorMOG2()
try:
    while True:
        ret, frame = cap.read()
        if ret == True:
            fgMask = backSub.apply(frame)
            cv.imshow('frame', frame)
            cv.imshow('fgMask', fgMask)
            fgMask = cv.threshold(fgMask, 25, 255, cv.THRESH_BINARY)[1]
            fgMask = cv.erode(fgMask, None, iterations=2, borderType=cv.BORDER_REPLICATE )
            contours = cv.findContours(fgMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            if(contours == []):
                update_sensor_message(False)
                print("No object continue moving")
            else:
                for cnt in contours:
                    #print(cv.contourArea(cnt))
                    if(cv.contourArea(cnt) < 1000 ):
                        update_sensor_message(False)
                        continue
                    else:
                        #print("Obstacle maann obsatcle")
                        update_sensor_message(True)
                
            
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break
        else:
            break

except KeyboardInterrupt:
    pass