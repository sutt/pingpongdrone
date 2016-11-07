import time, cv2

def log_run(**kwargs):
    fn = kwargs.get('fn', '')
    print 'logging'
    
class DisplayObj:
    
    def __init__(self,raw = True,**kwargs):
        self.raw = raw
        self.mirror = bool(kwargs.get('mirror', False))
        
        
    def display(self,frame,**kwargs):
        
        if kwargs.get('dontdisplay',False): return False
        
        frame2 = kwargs.get('frame2' , None)
            
        if not(self.raw) and ( frame2 is not None):
            frame_show = frame2
        else:
            frame_show = frame
            
        if kwargs.get('mirror',False):
            frame_show = cv2.flip(frame_show,1)
            
        cv2.imshow('frame',frame_show)
        
        #push this into log_run check
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        else:
            return False
                
class LoopObj:

    def __init__(self,**kwargs):
        self.i = 0
        self.time0 = time.time()
        self.timeout = kwargs.get('timeout', 5)
        self.t_frame = []
        self.cam_read_except_iter = 0
        
    def log_run(self,frame,**kwargs):
        
        try:
            self.i = self.i + 1
            time_i = time.time()
            inp_fps = kwargs.get('inp_fps',30)
            
            self.t_frame.append( (self.i,time_i) )
            
            if kwargs.get('Log',False):
                print str(self.i)
                
            if time_i - self.time0 > self.timeout:
                return True
            else:
                #print str(time_i - self.time0)
                return False
        except:
            return True
            
    def summarize_run(self,**kwargs):
        print 'i: ', str(self.i)
        print 'time: ', str(time.time() - self.time0)
            
    def cam_read_except(self,max_except = 10, e=None):
        self.cam_read_except_iter += 1
        if e is not None:
            print str(e)
        if self.cam_read_except_iter >= max_except:
            return True
        return False