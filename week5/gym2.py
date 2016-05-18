import gym,time, os, zmq,random, sys
from learning import Algo

def printer():
    print 'PQPWPWPQPPQW'

def createEnvNoisy(**kwargs):
    env =  gym.make('CartPole-v0')
    return env
    
def createEnv(**kwargs):
    old_stdout = sys.stdout 
    sys.stdout = open(os.devnull,"w")
    try:
        printer()
        env = gym.make('CartPole-v0')
    finally:
        sys.stdout.close()
        sys.stdout = old_stdout
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
        
    elif strat == 6:
    
        algo = kwargs.get('algo',None)
        
        action = algo.f(obs)
    
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
    
    if kwargs.get('env',False):
        env = kwargs.get('env',False)
    else:
        env = createEnvNoisy()
    env.reset()
    
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
                    #print 'returning'
                    return perfstrat
            
            
            env.reset()
            ind = 0
            
        if ind > int(kwargs.get('keepgoing',999)):
            return perfstrat
    
    
            
        
def evalGames(perf):        
    if not(perf):
        print 'no perf'
        return 0
    avgind = float(sum(perf)) / float(len(perf))
    return avgind

#import optparse
# p = optparse.OptionParser()
# p.add_option('--foo', '-f', default="yadda")
# p.add_option('--bar', '-b')
# options, arguments = p.parse_args()


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        
        algo = Algo()
        #need to set Beta[accel] to 1
        #algo.updateBeta([0,1,0,0])
        #algo.updateBetaFinal([0,1,0,0])
        
        env = createEnvNoisy()
        ind = 0
        
        while True:
        
            
            var = [0,1]  
            
            algo.reset_ygradient()
            for point in algo.build_gradient(vars = var):
                
                algo.updateBeta(point)
                
                perf = gameStrat(strat = 6, totalgames=50,Algo=algo, \
                                renderme = False, env = env)
                
                y = evalGames(perf)
                
                algo.update_ygradient(y)    
            
            #update algo
            updateB = algo.eval()
            algo.updateBetaFinal(updateB)
            
            
            print 'ind: ', str(ind), ' perf: ', str(algo._perf)
            print algo.BetaFinal
            
            #Exit Training Conditions
            ind += 1
            if algo._perf > 500:
                break
                
        #Print summary of loop outcome
        print str(algo.BetaFinal)
            

        
    else:
        for s in [1,2,3,4]:
            perf = gameStrat(strat = s, totalgames=5)
            eval = evalGames(perf)
            print eval
        
    