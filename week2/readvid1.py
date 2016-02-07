import numpy as np
import cv2
import argparse
import os, time, sys


ap = argparse.ArgumentParser()
ap.add_argument("--vidfile",  action = 'store',
                    default="ball-tracking/ball_tracking_example.mp4")
args = vars(ap.parse_args())



vc = cv2.VideoCapture(args["vidfile"])

while(vc.isOpened()):
    
    #print 'here'
    
    ret,frame = vc.read()
    
    if not(ret):
        break 
        
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        

print 'there'
vc.release()
cv2.destroyAllWindows()