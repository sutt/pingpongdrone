import gym,time, os, zmq,random
from learning import Algo

def createEnv(**kwargs):
    env = gym.make('CartPole-v0')
    return env

def playGame(env,**kwargs):
    
    inp = raw_input(disptxt)
            
    if inp == "q":
        action  = 0
    else:
        action = 1
    disptxt = "Last: " + str(action) + " ..."

    quad = env.step(action) 
    done = quad[2]

    return 'Game is done'
    
def strategize(obs,strat,**kwargs):
    
    a,b,c,d = obs
    env =  kwargs.get('env',None)
    
    if strat == 1:
        action = env.action_space.sample()
                    
    elif strat == 2:
        t= kwargs.get('t',None)
        action = 1 if (t % 2) == 0 else 0
    
    elif strat == 3:
        if env.state[2] > 0:
            action = 1
        else:
            action = 0
            
    elif strat == 4:
    
        angle1 = obs[2]
        accel1 = obs[1]
    
        if angle1 > 0:
            if accel1 > 1:
                action = 0
            else:
                action = 1
        else:
            if accel1 < -1:
                action  = 1
            else:
                action = 0

        
    elif strat == 5:
    
        algo = kwargs.get('algo',None)
        
        action = algo.makeDec(obs)
    
    return action
    
def logit(**kwargs):
    if kwargs.get('stratstart',False):
        print 'STRAT: ', str(kwargs.get('stratstart','None')), '------'
        return 1
        
    if kwargs.get('logloss',False):
        print 'You Lose on: ', str(kwargs.get('logloss','None'))
        return 1
        
    if kwargs.get('logstep',False) or gLogstep:
        state = kwargs.get('logstep',None)['state']
        state = map(lambda x: round(x,2), state)
        print state
        return 1
        
    return 1
    
def gameStrat(**kwargs):
        

    #Init strat
    strat = int(kwargs.get('strat',1))
    env = createEnv()
    logit(stratstart=strat)
    algo = kwargs.get('Algo',None)
    
    t0 = time.time()
    ind = 0
    
    #obs-memory
    perfstrat = []
    state = []
    
    while True:

        #play
        obs = env.state
        
        # strategize(env,extras = {previous obs, ind, etc...})
        action = strategize(obs,strat,env= env, t=ind, algo=algo)
        #logit(logstep = {'state':obs,'action':action})           
        
        #step
        quad = env.step(action)
        obs,reward,done,info = quad
        ind += 1
        
        #display
        if kwargs.get("renderme",True):
            env.render()
        
           
        #end playing
        if done:
            
            perfstrat.append(ind)
            
            if kwargs.get('continuesteps',False):
                if ind > int(kwargs.get('continuesteps',100)):
                    continue
            
            if kwargs.get('logendgame',False):
                logit(logendgame = {'ind':ind,'state':env.state})
            if kwargs.get('justone',False):
                return perfstrat
            
            if kwargs.get('totalgames',False):
                games = len(perfstrat)
                if games > int(kwargs.get('totalgames',1)):
                    print 'returning'
                    return perfstrat
            
            
            env.reset()
            ind = 0
            
        if ind > int(kwargs.get('keepgoing',999999999999)):
            return perfstrat
    
    
            
        
def evalGames(perf):        
    print perf
    avgind = float(sum(perf)) / float(len(perf))
    return avgind

import sys

#import optparse
# p = optparse.OptionParser()
# p.add_option('--foo', '-f', default="yadda")
# p.add_option('--bar', '-b')
# options, arguments = p.parse_args()


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        
        algo = Algo()
        #algo.update(delta_accel = 1,delta_angle = 0)
        ep = 0.1
        var = 1
        
        while True:
        
            var = [2]  
            for point in algo.build_gradient(vars = var):
                
                algo.updateF(point)
                
                perf = gameStrat(strat = 5, totalgames=3,Algo=algo)
                y = evalGames(perf)
                
                algo.update_ygradient(
            
            #update algo
            d = algo.eval(evals, var= var)
            
            algo.update(delta_accel = d['accel'],delta_angle = d['angle'])
            
            #if condition met:
                #break
                
        #Print summary of loop outcome
            

        
    else:
        for s in [1,2,3,4]:
            perf = gameStrat(strat = s, totalgames=5)
            eval = evalGames(perf)
            print eval
        
    