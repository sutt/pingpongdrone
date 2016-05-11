import gym,os,sys,time

class Algo():
    
    def __init__(self,**kwargs):
        self._accel = 0
        self._angle = 0
        
    def update(self,**kwargs):
        if kwargs.get('delta_accel',False):
            self._accel += kwargs.get('delta_accel',0)
        if kwargs.get('delta_angle',False):
            self._angle += kwargs.get('delta_angle',0)
            
    def makeDec(self, obs,**kwargs):
        angle1 = obs[2]
        accel1 = obs[1]
    
        if angle1 > self._angle:
            if accel1 > self._accel:
                action = 0
            else:
                action = 1
        else:
            if accel1 < -(self._accel):
                action  = 1
            else:
                action = 0
                
        return action