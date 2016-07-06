import gym,os,sys,time, random

class Algo():
    
    def __init__(self,**kwargs):
        
        self._obs = [0,0,0,0]
        
        #X can different from obs, e.g. Xi = abs(obs[i])
        if kwargs.get('Xtransform',False):
            self.X = self._obs   
        else:
            self.X = self._obs   #set X to the true size vec
        self.dimX = len(self.X)
        
        #Beta(i) for each i in X
        self.Beta = [0 for i in range(self.dimX)]
        #Final holds the current best values
        self.BetaFinal = [0 for i in range(self.dimX)]

        
        #best perf, current perf, [0,inf), higher is better 
        self._perf = 0
        

        
        #points in Beta-Space
        self.beta_gradient = [0 for i in range(self.dimX)]
        
        #points in Xspace
        self.x_gradient = []  
        
        #for each el in betagradient, a correspoing  y(beta(i)) 
        self.y_gradient = []
        
        self.y_misc = []
        
        
    def updateBeta(self,point,**kwargs):
        self.Beta = point
    
    def updateBetaFinal(self,point,**kwargs):
        self.BetaFinal = point
        
    def update_ygradient(self, y_eval,**kwargs):
        if not(y_eval):
            self.y_gradient.append([])
        else:
            self.y_gradient.append(y_eval)
    
    def update_ymisc(self, ymisc,**kwargs):
        if not(ymisc):
            self.y_misc.append([])
        else:
            self.y_misc.append(ymisc)
            
    def reset_ygradient(self):
        self.y_gradient = []
    
    def reset_ymisc(self):
        self.y_misc = []
    
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
        
    def f(self,obs,**kwargs):
        angle1 = obs[2]
        accel1 = obs[1]
        pos1 = obs[0]
        
        _pos = self.Beta[0]
        _accel = self.Beta[1]
        _angle = self.Beta[2]
        _posB = self.Beta[3]
        
        if angle1 > _angle:
            if accel1 > _accel:
                action = 0
            else:
                action = 1
        else:
            if accel1 < -_accel:
                action  = 1
            else:
                action = 0
        
        if pos1 >  _pos:
            action = action if random.uniform(0,1) > _posB else int(not(action))
        if pos1 <  -_pos:
            action = action if random.uniform(0,1) > _posB else int(not(action))
        
        #time.sleep(.5)
        #print str(round(obs[1],2)), " - " , str(round(obs[2],2))
        #print action
        return action
    
    
    def evalexpectations(self,perf):        
        if len(perf) < 1:
            return 0
        return float(sum(perf)) / float(len(perf))
        
        
    def eval(self,**kwargs):
        
        l = kwargs.get('l', 1.0)   #learning rate
        
        yg = self.y_gradient
        Bg = self.beta_gradient
        
        #Perf metric
        y1 = map(lambda x: self.evalexpectations(x),yg)
        
        #Max Perf
        indYmax = y1.index(max(y1))
        self._perf = max(y1)
        
        #log series of games
        if kwargs.get('logbestrun',False):
            print self.y_gradient[indYmax]
            #pass
        
        if kwargs.get('logbestrunloss',False):
            if self._perf > 300 or True:
                s = str(self.y_misc[indYmax])
                #s = str("\n".join(self.y_misc[indYmax]))
                print 'Best run loss: ', s
                pass
        
        #Based on Change, find new Betas
        xn = self.dimX
        B0 = self.BetaFinal
        B1 = Bg[indYmax]
        
        Bnew = [ float( B0[i] + float((B1[i] - B0[i])*l) ) \
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
        
        if vars:
            return self.permute_variables(points2,vars)
        return points2
        
    def build_gradient(self,**kwargs):
        """self._Beta + g(i) for all i in combination(vars)"""
        
        eps = kwargs.get('eps',[0.2]*self.dimX)
        vars = kwargs.get('vars',range(self.dimX))
        
        dvars = []
        for i in range(len(vars)):
            var = vars[i]
            ep = eps[i]
            dvars.append((var, [float(-1*ep),float(1*ep)]))
        
        #start with 0 or 1 point to permute
        origin = []
        if not(kwargs.get('no_origin',False)):
            origin.append(self.BetaFinal)
        
        points = self.permute_variables(origin,dvars)
        
        self.beta_gradient = points
        return points
        
        
        
        