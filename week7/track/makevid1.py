from collections import deque
import numpy as np
import argparse
import imutils
import cv2

from src.track import TrackObj
from src.camera import MyCam
from src.draw import DrawObj
from src.utils import log_run
from src.utils import DisplayObj, LoopObj
#python makevid1.py --showvid  --

ap = argparse.ArgumentParser()
ap.add_argument("--externalcam", action="store_true", default=False)
ap.add_argument("--dontsave", action="store_false", default=True)
ap.add_argument("--unlocaldir", action="store_true", default=False)
ap.add_argument("--showvid", action="store_true", default=False)
ap.add_argument("--ext", default = ".avi")
args = vars(ap.parse_args())


def vid():
    
    cam  =  MyCam( device_num = int(args["externalcam"]) )
    #cam.set_params(toggleframe=True)    
    cam.get_params(Log=True)
    cam.setup_save_video(ext=".avi",Log=True)
    
    to = TrackObj()
    do = DrawObj()
    dispobj = DisplayObj(raw=False)
    loop = LoopObj(timeout = 20)
    
    while(cam.cam.isOpened()):
        try:
            ret,frame = cam.cam.read()  #make this method and time it
            if ret:
                to.track_obj(frame, min_radius = 10)
                do.draw_onto_frame(frame, to.center, to.radius)
                if dispobj.display(frame=frame,frame2=do.frame2): break
                cam.save_video_frame(frame)
                if loop.log_run(frame): break
        except:
            if loop.cam_read_except(): break
                
    cam.cleanup_cam(Log=True)
    cv2.destroyAllWindows()  #move this into disp.clean loop.clean
    log_run()
    return 1
    
vid()