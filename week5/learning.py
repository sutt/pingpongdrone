import gym,os,sys,time, random

class Algo():
    
    def __init__(self,**kwargs):
        self._accel = 0
        self._angle = 0
        self._pos = 0
        
        self._obs = [0,0,0,0]
        self.dimX = len(self._obs)
        
        #best perf, current perf, [0,inf), higher is better 
        self._perf = 0
        
        #{x1:[v[0],v[1],...v[n]], x2:..}
        self.x_gradient = {}  
        
        #{x1:[y[x0],y[x1],...y[xn]], x2:..}
        self.y_gradient = {}
        
        
        
    def updateF(self,**kwargs):
        if kwargs.get('delta_accel',False):
            self._accel += kwargs.get('delta_accel',0)
            self._obs[1] += kwargs.get('delta_accel',0)
        if kwargs.get('delta_angle',False):
            self._angle += kwargs.get('delta_angle',0)
            self._obs[2] += kwargs.get('delta_angle',0)
        
        if kwargs.get('new_obs',False):
            self._obs = new_obs
        return 1
        
    def update_ygradient(self,xgrad_point, y_eval,**kwargs):
        
        #self.y_gradient = 1
        
        return 1
    
    def reset_ygradient(self,**kwargs):
        self.y_gradient = {}
    
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
        
    def f(self,**kwargs):
        return 1
        
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
    
    
    #@staticmethod
    def permute_variables(self,points,vars,**kwargs):
        #while True:
        var = vars.pop()
        v, vals = var[0],var[1]
        points2 = points[:]
        
        cur = self._obs[:]
        x_n = len(self._obs)
        
        print 'in'
        ind = 0
        
        for p_0 in points[:]:
            print 'p_0', str(p_0)
            for val in vals:
                
                print 'v:', str(val)
                
                cur = p_0[:]
                point = [cur[i] + val if i == v else cur[i] \
                         for i in range(x_n)]
                points2.append(point)
                print 'P:' , str(point)
                    
                #ind += 1
                #if ind > 16: 
                    #return points2
        print points2
        
        if len(vars) < -1:
            print 'ret'
            print points2
        if len(vars) > 0:
            print 'recurse'
            points = self.permute_variables(points2,vars)
            return points

        #print 'end while iter'
        print 'end func'
        return points2
        
    def build_gradient(self,**kwargs):
        """self._obs + g(i) for all i in combination(vars)"""
        
        ep = float(kwargs.get('ep',0.1))
        vars = kwargs.get('vars',[0])
        dvars = []
        for var in vars:
            dvars.append(var, [float(-1*ep),float(-1*ep)])
        
        current = self._obs[:]
        points = self.permute_variables([current],dvars)

        #{var_ind1 : [var
        #return a flattened version
        return points
        
        
        
        