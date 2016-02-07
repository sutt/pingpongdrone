import numpy as np
import cv2
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--fpslog", type=int, default=0)
ap.add_argument("--ilog", type=int, default=0)
ap.add_argument("--fps10", type=int, default=0)
ap.add_argument("--displayoff", type=int, default=0)
ap.add_argument("--getsize", action="store_true", default=False)
args = vars(ap.parse_args())

i  = 1
c = time.time()
_fps = []

cap = cv2.VideoCapture(0)

while(True):
    
    a = time.time()
    
    ret, frame = cap.read()
    
    if args["getsize"]:
        fsize = frame.shape
        print fsize
    
    if not(args["displayoff"]):
        
        
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('frame',gray)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    i = i + 1
    if args["ilog"]:
        print i
        
    b = time.time()
    _fps.append((1/(b - a)))
    if args["fpslog"]:
        print (1/(b - a))
        
    if args["fps10"]:
        if (b - c) > 10:
            print i
            print 'avg: ', str(float(sum(_fps))/float(i - 1))
            break
    
    
cap.release()
cv2.destroyAllWindows()