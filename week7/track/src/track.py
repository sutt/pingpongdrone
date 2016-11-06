# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
ap.add_argument("-c", "--camera", type=int, default=0,
        help="0 for laptopcam 1 for external")
ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
ap.add_argument("-m", "--mirror", type=int, default=0,
        help="mirror image display, use 1")
args = vars(ap.parse_args())

pts = deque(maxlen=args["buffer"])


class TrackObj:

    def __init__(self):

        self.greenLower = greenLower = (29, 86, 6)
        self.greenUpper = greenUpper = (64, 255, 255)
        self.buffer = 128
        self.center = None
        self.radius = None
        self.center_dic = {}
        self.radius_dic = {}


    def track_obj(self,frame, **kwargs):
        
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        center = None
        radius = None

        if len(cnts) > 0:

            # the minimum enclosing circle and centroid
            #this is where you select only one object
            c = max(cnts, key=cv2.contourArea)
            
            #x,y is different from center
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        if radius >= kwargs.get('min_radius',1):
            self.center = center
            self.radius = radius
        else:
            self.center = None
            self.radius = None
            
        return (center, radius)
        
        
   