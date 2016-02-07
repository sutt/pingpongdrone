import numpy as np
import cv2


path = "C:/Users/William/Desktop/drone/week1/ball-tracking/ball_tracking_example.mp4"
path = "ball-tracking/ball_tracking_example.mp4"
path ="ball-tracking/tree.avi"
cap = cv2.VideoCapture(path)
i = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    print ret
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',frame)
    i+=1
    print i
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()