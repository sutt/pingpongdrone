import numpy as np
import cv2
import os, sys, time
from collections import deque

class DrawObj:

    def __init__(self, buffer = 128):
        self.buffer = buffer
        self.pts = deque(maxlen = buffer)  #this should be in trackobj
        self.current_frame = None
        self.frame2 = None
        
    def set_current_frame(self,frame):
        self.current_frame = frame
    
    def draw_onto_frame(self,inp_frame, center,radius):
        try:
            frame = inp_frame.copy()        
            buffer = self.buffer
            
            if (center != None) and (radius != None):
                cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
            self.pts.appendleft(center)
            for i in xrange(1, len(self.pts)):
                #a discontinuity in finding will cause
                if self.pts[i - 1] is None or self.pts[i] is None:
                    continue
                
                thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
                
                cv2.line(frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)
                
            self.frame2 = frame
        except:
            print 'unable to draw'
            self.frame2 = None
        