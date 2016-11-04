import numpy as np
import cv2
import argparse
import os, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--showvid", action="store_true", default=False)
ap.add_argument("--showsize", action="store_true", default=False)
ap.add_argument("--dontsave", action="store_false", default=True)
ap.add_argument("--dontrecord", action="store_false", default=True)
ap.add_argument("--getcam", action="store_true", default=False)
ap.add_argument("--setcam", action="store_true", default=False)
ap.add_argument("--setgain", action="store_true", default=False)
ap.add_argument("--logfps", action="store_true", default=False)
ap.add_argument("--toggleframe", action="store_true", default=False)
ap.add_argument("--unlocaldir", action="store_true", default=False)
ap.add_argument("--device", type=int, default=0, help = "1 for ext")
ap.add_argument("--timeout", type=int, default=3, help = "1 for ext")

ap.add_argument("--codec", default="")
ap.add_argument("--ext", default = ".avi")
	
args = vars(ap.parse_args())

path_to_uservideos = "C:\Users\William\Videos\\" 


#Video Options

cd = args["codec"]
if  cd == "" :
    fourcc = -1
else:
    fourcc = cv2.VideoWriter_fourcc(cd[0],cd[1],cd[2],cd[3])
    #fourcc = cv2.VideoWriter_fourcc("M","P","4"," ")
    #Logitech Video I420 works
    #default:-466162819.0
    #divx, xvid, h264, x264, mjpg, wmv?
    

_fw = cv2.CAP_PROP_FRAME_WIDTH 
_fh = cv2.CAP_PROP_FRAME_HEIGHT
_fps = cv2.CAP_PROP_FPS
_fourcc = cv2.CAP_PROP_FOURCC

_params = [_fw,_fh,_fps,_fourcc]

if args["setcam"]:
    outshape = (1920,1080)
    outfps = 1000    
else:
    outshape = (640,480)
    outfps = 30
#outshape = (640,480)

#WriteVideo
if args["dontsave"]:
    i = 0
    if args["unlocaldir"]:
        files= os.listdir(path_to_uservideos)
    else:
        files = os.listdir(os.getcwd())
        
    while(True):
        i += 1
        fn = "output" + str(i)
        fn += args["ext"] 
            
        if fn in files:
            continue
        else:
            if args["unlocaldir"]:
                fn = path_to_uservideos + fn
                
            out = cv2.VideoWriter(fn,fourcc,outfps,outshape)    
            break


#Caemra Object            
cam  =  cv2.VideoCapture(args["device"])

if args["getcam"]:
    _cam = [cam.get(p) for p in _params]
    print _cam

if args["setcam"]:
    
   # First set codec, then fps, then h/w #http://stackoverflow.com/questions/16092802/capturing-1080p-at-30fps-from-logitech-c920-with-opencv-2-4-3
    if args["toggleframe"]:
        try:
            rrr,fff = cam.read()
        except:
            print 'couldnt toggle'
        
    #cam.set(_fourcc,fourcc)
    
    #cam.set(_fourcc,cam.get(_fourcc))
    #_I420 2304,1536, fps=2
    cam.set(_fps,30)
    
    #cam.set(_fw,1920)
    #cam.set(_fh,1080)
    
    _cam = [cam.get(p) for p in _params]
    print _cam

if args["setgain"]:
    cam.set(cv2.CAP_PROP_GAIN,255)
    print cam.get(cv2.CAP_PROP_GAIN)
    cam.set(cv2.CAP_PROP_EXPOSURE,-5)
    print cam.get(cv2.CAP_PROP_EXPOSURE)
    cam.set(cv2.CAP_PROP_BRIGHTNESS,128)
    print cam.get(cv2.CAP_PROP_BRIGHTNESS)
    
#Record Video
if args["dontrecord"]:

    a = time.time()
    i = 0
    while(cam.isOpened()):
        
        
        try:
            a2 = time.time()
            ret,frame = cam.read()
            
            if ret:

                if args["showsize"]:
                    print frame.shape
            
                if args["dontsave"]:
                    out.write(frame)

                if args["showvid"]:
                    cv2.imshow('frame',frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                if args["logfps"]:
                    #print float(1.0) / float(time.time() - a2)
                    i += 1
                
            if (time.time() - a) > args["timeout"]:
                print 'done with i = ', str(i)
                break
        except:
            print 'excepted'
            break

#Clean up        
cam.release()
try:
    out.release()
except:
    print 'no out to release'

if args["dontsave"]:
    print fn, ": ", str(os.path.getsize(fn) / (1000)), " kb"
