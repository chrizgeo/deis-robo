import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

_, first_frame = cap.read()
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    difference = cv2.absdiff(first_gray, gray_frame)
    threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)

    cv2.imshow("First frame", first_frame)
    cv2.imshow("Frame", frame)
    cv2.imshow("difference", difference)
    cv2.imshow("Threshold", threshold)

    contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if(contours == []):
        print("No object continue moving")
    else:
        for cnt in contours:
            print(cv2.contourArea(cnt))
            if(cv2.contourArea(cnt) < 2300 ):
                continue
            
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("Object Detected stop moving")
    
    key = cv2.waitKey(1)
    if(key == 27):
        break

cap.release()
cv2.destroyAllWindows()