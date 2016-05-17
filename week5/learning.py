import gym,os,sys,time, random

class Algo():
    
    def __init__(self,**kwargs):
        
        self._obs = [0,0,0,0]
        
        #X can different from obs, e.g. Xi = abs(obs[i])
        if kwargs.get('Xtransform',False):
            self.X = self._obs   
        else:
            self.X = self._obs
        self.dimX = len(self.X)
        
        #Beta(i) for each i in X
        self.Beta = [0 for i in range(self.dimX)]
        #Final holds the current best values
        self.BetaFinal = [0 for i in range(self.dimX)]
        
        
        
        #best perf, current perf, [0,inf), higher is better 
        self._perf = 0
        
        #how the deltas in 
        self.Beta_gradient = [(i,(0)) for i in range(self.dimX)]
        
        #{x1:[v[0],v[1],...v[n]], x2:..}
        self.x_gradient = []  
        
        #{x1:[y[x0],y[x1],...y[xn]], x2:..}
        self.y_gradient = []
        
        
        
    def updateBeta(self,point,**kwargs):
        self.Beta = point
    
    def updateBetaFinal(self,point,**kwargs):
        self.BetaFinal = point
        
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
    
    
    def evalGames(self,perf):        
        avgind = float(sum(perf)) / float(len(perf))
        return avgind

        
    def eval(self,**kwargs):
        
        l = kwargs.get('l', 1.0)   #learnign rate
        
        yg = self.y_gradient
        xg = self.x_gradient
        
        #Max Perf
        indYmax = yg.index(max(yg))
        
        #Based on Change, find new Betas
        xn = self.dimX
        B0 = self.BetaFinal
        B1 = xg[indYmax]
        
        Bnew = [ float( B0[i] + float((B1[i] - B0[i])*l) \
                  for i in range(xn)]

        return Bnew
    
    
    def permute_variables(self,points,vars,**kwargs):
        """Beta(i) + delta(i,j) for all i, j in:
                vars= [ (i1,(j1,j2,...)), (i2,(j1,j2,...)), ... ] 
            Returns: list of points, vectors in Beta-space  """
                
        var = vars.pop()
        v, vals = var[0],var[1]

        points2 = points[:] 
        
        #no origin 
        if len(points) == 0:
            iter_p = [self.BetaFinal]
        else:
            iter_p = points[:]
            
        for p in iter_p:
            for val in vals:
                
                point = [p[i] + val if i == v else p[i] \
                         for i in range(len(self._obs))]
                points2.append(point)
        
        if len(vars) > 0:
            return self.permute_variables(points2,vars)
        return points2
        
    def build_gradient(self,**kwargs):
        """self._Beta + g(i) for all i in combination(vars)"""
        
        ep = float(kwargs.get('ep',0.1))
        vars = kwargs.get('vars',[0])
        dvars = []
        for var in vars:
            dvars.append((var, [float(-1*ep),float(-1*ep)]))
        
        self.Beta_gradient = dvars[:]
        #start with 0 or 1 point to permute
        origin = []
        if not(kwargs.get('no_origin',False)):
            origin.append(self.BetaFinal)
        
        points = self.permute_variables(origin,dvars)

        return points
        
        
        
        