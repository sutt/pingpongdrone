import gym,os,sys,time, random

class Algo():
    
    def __init__(self,**kwargs):
        self._accel = 0
        self._angle = 0
        self._pos = 0
        self._obs = [0,0,0,0]
        
    def update(self,**kwargs):
        if kwargs.get('delta_accel',False):
            self._accel += kwargs.get('delta_accel',0)
            self._obs[1] += kwargs.get('delta_accel',0)
        if kwargs.get('delta_angle',False):
            self._angle += kwargs.get('delta_angle',0)
            self._obs[2] += kwargs.get('delta_angle',0)
            
    def makeDec(self, obs,**kwargs):
        angle1 = obs[2]
        accel1 = obs[1]
        pos1 = obs[0]
        
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
        
    def eval(self,evals,**kwargs):
        delta = {'accel': 0,'angle' :0}
        
        l = kwargs.get('l', 1)
        ep = float(kwargs.get('ep',0.1))
        
        eval_low,eval_high = evals[0],evals[1]
        sign = -1 if eval_low > eval_high else 1
        
        if kwargs.get('var',  0) == 1:
            delta['accel'] += float(sign * l * ep)
        if kwargs.get('var', 0) == 2:
            delta['angle'] += float(sign * l * ep)
        
        return delta
        
    def gradient(self,var,**kwargs):
        
        ep = float(kwargs.get('ep',0.1))
        #var = kwargs.get('var',1)
        current = self._obs[var]
        trylow,tryhigh = current - ep, current + ep
        
        return (trylow,tryhigh)