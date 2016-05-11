import gym,time, os, zmq,random


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
        action = 1 if (t % 2) == 0 else 0
    
    elif strat == 3:
        if env.state[2] > 0:
            action = 1
        else:
            action = 0
            
    elif strat == 4:
    
        angle1 = env.state[2]
        accel1 = env.state[1]
    
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
    
        angle0 = angle1
        accel0 = accel1
        
    elif strat == 5:
    #else:
    
        xx = [0,1,2,3,4,10,20,30,100][strat]
        angle1 = env.state[2]
        accel1 = env.state[1]
        pos1 = env.state[0]
        
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
        
        if (abs(pos1) > 1) & (abs(accel1) > .6):
            bench = abs(pos1) - 1
            bench = int(bench * 10)
            
            #if random.randint(1,xx) < bench :
            if random.randint(1,10) < 1 :
                action = (action - 1)*(-1)
    
    return action
    
def logit(**kwargs):
    if kwargs.get('stratstart',False):
        print 'STRAT: ', str(kwargs.get('stratstart','None')), '------'
        
    if kwargs.get('logloss',False):
        print 'You Lose on: ', str(kwargs.get('logloss','None'))
        
    if kwargs.get('logstep',False):
        state = kwargs.get('logstep',None)['state']
        state = map(lambda x: round(x,2), state)
        print state
    
    return 1
    
def gameStrat(**kwargs):
        

    #Init strat
    strat = int(kwargs.get('strat',1))
    env = createEnv()
    logit(stratstart=strat)
    
    t0 = time.time()
    ind = 0
    
    #obs-memory
    perfstrat = []
    state = []
    
    while True:

        #play
        obs = env.state
        action = strategize(obs,strat,env= env)
        #logit(ind = ind, obs = obs, action = action)           
        
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
            
            if kwargs.get('logendgame',False):
                logit(logendgame = {'ind':ind,'state':env.state})
            if kwargs.get('justone',False):
                return perfstrat
            if kwargs.get('keepgoing',False):
                if ind > int(kwargs.get('keepgoing',100)):
                    return perfstrat
            else:
                env.reset()
            
        if ind > int(kwargs.get('keepgoing',999999999999)):
            return perfstrat
    
    
            
        
def evalGames(perf):        
    print perf
    avgind = float(sum(perf)) / float(len(perf))
        

import sys

#import optparse
# p = optparse.OptionParser()
# p.add_option('--foo', '-f', default="yadda")
# p.add_option('--bar', '-b')
# options, arguments = p.parse_args()

if __name__ == "__main__":
    
    perf = gameStrat(strat = 1, justone=True)
    eval = evalGames(perf)
    print eval
    
    