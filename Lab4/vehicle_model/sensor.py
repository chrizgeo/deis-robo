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
global last_obstacle
global isMoving

last_timestamp = 0
isMoving = False

def update_sensor_message(shouldBrake):
    print(f'Publish on SENSOR channel \ {shouldBrake}.')
    global last_timestamp
    sensor_message.timestamp =  int(time.time()*1000)
    sensor_message.detected_obstacle = shouldBrake
    if(sensor_message.timestamp - last_timestamp > 10):        
        lc.publish("SENSOR", sensor_message.encode())
        last_timestamp = sensor_message.timestamp
        last_obstacle = sensor_message.detected_obstacle

cap = cv.VideoCapture(0)
# take first frame of the video
ret,frame = cap.read()
backSub = cv.createBackgroundSubtractorKNN()
try:
    while True:
        ret, frame = cap.read()
        if ret == True:
            fgMask = backSub.apply(frame)
            cv.imshow('frame', frame)
            fgMask = cv.threshold(fgMask, 25, 255, cv.THRESH_BINARY)[1]
            fgMask = cv.erode(fgMask, None, iterations=2, borderType=cv.BORDER_REPLICATE )
            #fgMask = cv.dilate(fgMask, None, iterations=2, borderType=cv.BORDER_REPLICATE )
            cv.imshow('fgMask', fgMask)
            contours = cv.findContours(fgMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            if(contours == []):
                update_sensor_message(False)
                print("No object continue moving")
            else:
                total_area = 0
                for cnt in contours:
                    total_area  = total_area + cv.contourArea(cnt)
                    #print(cv.contourArea(cnt))
                if(total_area < 1000 ):
                    update_sensor_message(False)
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