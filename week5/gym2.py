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

def roundlist(inp,**kwargs):
    r = kwargs.get('r',0)
    return str([round(x,r) for x in inp])
    
def explainloss(state,**kwargs):
    #print state
    angle,pos = state[2], state[0]   #.21
    _angle,_pos = 15. * 3.14159 * 2. / 360. , 2.4
    #0.25821287671232873
    if (abs(angle) > _angle) & (abs(pos) > _pos):
        return 3
    if abs(angle) > _angle:
        return 1
    if abs(pos) > _pos:
        return 2
    #s = "\n".join([str(i)+": "+str(v)[:6] for i,v in enumerate(state)])
    s = str(state[2])[:5]+"\n"
    
    #oh! because you've recovered in state(s) from state(s-1), explain loss from state(s-1)?
    #print s
    return 0
    #s = "\n".join([str(i)+": "+str(v)[:4] for i,v in enumerate(state)])
    #return s
    
def logit(**kwargs):
    if kwargs.get('stratstart',False):
        print 'STRAT: ', str(kwargs.get('stratstart','None')), '------'
        return 1
        
    if kwargs.get('logloss',False):
        print 'You Lose on: ', str(kwargs.get('logloss','None'))
        return 1
        
    if kwargs.get('logstep',False): # or gLogstep:
        state = kwargs.get('logstep',None)['state']
        state = map(lambda x: round(x,2), state)
        print state
        return 1
    
    if kwargs.get('logendgame',False):
        state = kwargs.get('logstep',None)['state']
        loss = explainloss(state)
        
        
    if kwargs.get('logMt',False) :
        inp = kwargs.get('logMt',False)
        ind, algo = inp[0], inp[1]
        s_perf = roundlist([algo._perf])
        s_beta = roundlist(algo.BetaFinal, r = 2)
        
        s_out = "ind: "+str(ind)+" "*(5 - len(str(ind)))+s_beta+"  perf: "+s_perf
        print s_out
        
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
    lossreason = []
    
    while True:

        #play
        obs0 = env.state
        
        # strategize(env,extras = {previous obs, ind, etc...})
        action = strategize(obs0,strat,env= env, t=ind, algo=algo)
        #logit(logstep = {'state':obs,'action':action})           
        
        #step
        quad = env.step(action)
        obs,reward,done,info = quad
        ind += 1
        
        #display
        if kwargs.get("renderme",True):
            env.render(close=True)
        
           
        #end playing
        if done:
            
            perfstrat.append(ind)
            lossreason.append(explainloss(obs))
            
            if kwargs.get('continuesteps',False):
                if ind > int(kwargs.get('continuesteps',100)):
                    continue
            
            if kwargs.get('logendgame',False):
                logit(logendgame = {'state':env.state,'state0':obs0})
                
                
            if kwargs.get('justone',False):
                return perfstrat
            
            if kwargs.get('totalgames',False):
                games = len(perfstrat)
                if games >= int(kwargs.get('totalgames',1)):
                    #print 'returning'
                    return {'perf': perfstrat,  'loss': lossreason}
                            
            
            
            env.reset()
            ind = 0
            
    return 0

    

#import optparse
# p = optparse.OptionParser()
# p.add_option('--foo', '-f', default="yadda")
# p.add_option('--bar', '-b')
# options, arguments = p.parse_args()


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        
        algo = Algo()
        #cheats, init-Betas
        algo.updateBetaFinal([0,0,0,.1])
        
        env = createEnvNoisy()
        ind = 0
        
        while True:
        
            
            var = [0,1,2,3]  
            ep = [0.2,0.1,.005,0.01]
            
            algo.reset_ygradient()
            algo.reset_ymisc()
            for point in algo.build_gradient(vars = var, eps = ep):
                
                algo.updateBeta(point)
                
                ret = gameStrat(strat = 6, totalgames=50,Algo=algo, \
                                renderme = True, env = env)
                
                
                algo.update_ygradient(ret['perf'])   
                algo.update_ymisc(ret['loss'])
                
            #update algo
            updateB = algo.eval(l = 0.5, logbestrun=True, logbestrunloss=True)
            algo.updateBetaFinal(updateB)
            
            
            logit(logMt = (ind, algo))
            
            #Exit Training Conditions
            ind += 1
            if algo._perf > 5000:
                break
                
        #Print summary of loop outcome
        print str(algo.BetaFinal)
            
        
        
    else:
        for s in [1,2,3,4]:
            perf = gameStrat(strat = s, totalgames=5)
            eval = evalGames(perf)
            print eval
        
    