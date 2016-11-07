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
    
    cam  =  MyCam( device_num = int(args["externalcam"]), savevid = False )
    cam.get_params(Log=True)
    cam.set_params(toggleframe=True, fps = 30)    
    cam.get_params(Log=True)
    cam.setup_save_video(ext=".avi",Log=True,fps = 30)
    
    to = TrackObj()
    do = DrawObj()
    dispobj = DisplayObj(raw=False)
    loop = LoopObj(timeout = 10)
    
    while(cam.cam.isOpened()):
        try:
            ret,frame = cam.cam.read()  #make this method and time it
            if ret:
                print str(frame.shape)
                to.track_obj(frame, min_radius = 10)
                do.draw_onto_frame(frame, to.center, to.radius)
                if dispobj.display(frame=frame,frame2=do.frame2, mirror = True, dontdisplay = True): break
                cam.save_video_frame(frame)
                if loop.log_run(frame, Log=False): break
        except Exception as e:
            if loop.cam_read_except(e=e): break
                
    cam.cleanup_cam(Log=True)
    cv2.destroyAllWindows()  #move this into disp.clean loop.clean
    loop.summarize_run()    
    return 1
    
vid()
