import numpy as np
import cv2
import argparse
import os, sys, time
from sys import path

path_to_uservideos = "C:\Users\William\Videos\\" 

class MyCam:

    def __init__(self,device_num = 0,savevid = True):
        self.cam = cv2.VideoCapture(device_num)
        self.savevid = savevid
        self.vidWriter = None
        self.vw_fourcc = -1
        self.cam_params = {}
        
    def get_params(self, **kwargs):
        
        _fw = cv2.CAP_PROP_FRAME_WIDTH 
        _fh = cv2.CAP_PROP_FRAME_HEIGHT
        _fps = cv2.CAP_PROP_FPS
        _fourcc = cv2.CAP_PROP_FOURCC
        
        _params = [_fw,_fh,_fps,_fourcc]
        
        ret = [self.cam.get(p) for p in _params]
        
        if kwargs.get('Log',False):
            print ret
        
        return ret
    
    def set_vw_fourcc(self,cd,**kwargs):
        #cd = "x264"
        self.vw_fourcc = cv2.VideoWriter_fourcc(cd[0],cd[1],cd[2],cd[3])
        #fourcc = cv2.VideoWriter_fourcc("M","P","4"," ")
        #Logitech Video I420 works
        #default:-466162819.0
        #divx, xvid, h264, x264, mjpg, wmv?

    def set_params(self, arg, **kwargs):
    
       # First set codec, then fps, then h/w #http://stackoverflow.com/questions/16092802/capturing-1080p-at-30fps-from-logitech-c920-with-opencv-2-4-3
        if kwargs.get('toggleframe', False):
            try:
                rrr,fff = cam.read()
            except:
                print 'couldnt toggle'
            
        #cam.set(_fourcc,fourcc)
        #cam.set(_fourcc,cam.get(_fourcc))
        #_I420 2304,1536, fps=2
        #cam.set(_fps,30)
        #cam.set(_fw,1920)
        #cam.set(_fh,1080)
        
        if kwargs.get('setsize',False):
            outshape = (1920,1080)
            outfps = 1000    
        else:
            outshape = (640,480)
            outfps = 30
        
    
    def setup_save_video(self,**kwargs):
        """ optional args: dir ext Log """
        
        outfps,outshape = 30, (640,480)
        self.set_vw_fourcc('x264')
        
        if len(kwargs.get('dir','')):
            path =  kwargs.get('dir', '')
        else:    
            path = os.path.join(os.getcwd(), 'data')    
        
        files= os.listdir(path)
        files = map(lambda fstr: (fstr.split("."))[0], files)
        
        i = 0
        while(True):
            i += 1
            fn = "output" + str(i)
            fn += kwargs.get("ext",".avi") 
                
            if fn in files:
                continue    
            else:
                path_fn = os.path.join(path,fn)    
                vidWriter = cv2.VideoWriter(path_fn, self.vw_fourcc,outfps,outshape)
                break    
                
        self.vidWriter = vidWriter
        if kwargs.get('Log',False):
            print vidWriter
            
    def save_video_frame(self,frame,**kwargs):
        if not(self.savevid):
            return 0
        try:
            self.vidWriter.write(frame)
        except:
            return 0
        
    def cleanup_cam(self, **kwargs):
        self.cam.release()
        if self.vidWriter != None:
            try:
                self.vidWriter.release()
            except:
                print 'couldnt release vidwriter'
                
        if kwargs.get('Log',False):
            try:    
                print 'camera is released: ', str(cam.cam.isOpened())
            except:
                print 'couldnt log camera release'

