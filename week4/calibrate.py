import sys
import serial
import time

from imports.Motor import Motor2 as Motor
from imports.Motor import MySerialLock as MySerial    
    

    
## Calibration Program Flow #######################

def pause(dispTxt, breaker):
    while(True):
        inp = raw_input(dispTxt)
        if any(keywords in inp for keywords in breaker):
            return inp
        else:
            print 'cmd not recognized'
            
    
def parseQW(cmd):
    """cmd of form <q> <N> or <qqq...q> """
    words = cmd.split(' ')
    if len(words) > 1:
        return int(words[1])
    return max( [ words[0].count(s) for s in ["q","w"]] )
    
def parseA(cmd):
    """cmd of form <a> <decimal> e.g. a .00025 """
    words = cmd.split(' ')
    if len(words) > 1:
        return str(words[1])
    return "0"
    

###Calibration ManualRun #############################    

def motorInit2(Ser):
    """ this sets up motor from class """
    pause('Y to continue ...', ['Y'])
    MyMotor = Motor(Ser)
    return MyMotor

def motorInit(Ser):
    """ this sets up motor from class """
    pause('Y to continue ...', ['Y'])
    MyMotor = Motor(Ser)
    MyMotor.on()
    return MyMotor
    
def calibrateMotor(Motor1):
        
    #Now loop untill configured
    while(True):
        
        ret = pause('q to release, w to wind ...', ['q','w','exit', 'reversedir','setwindmax','p','o', 'outputlog', 'a'])

        
        #respond to input ---------------
        if ret[0] == 'q':
            retsteps = parseQW(ret)
            Motor1.up(steps = retsteps, log=False)
            print str(retsteps)
        
        if ret[0] == 'w':
            retsteps = parseQW(ret)
            Motor1.down(steps = retsteps, log=False)
            print str(retsteps)
            
        if ret == 'reversedir':
            Motor1.windDir = -1*(Motor1.windDir - 1)
        
        if ret == 'outputlog':
            Motor1.outputlog()
        
        if ret == 'setwindmax':
            Motor1.setWindMax()
            print 'wound, stepind: ', str(Motor1.stepInd)
        
        if ret[0] == 'a':
            print 'a cmd'
            strVal = parseA(ret)
            if strVal != "0":
                #method below will convert to float or fail
                Motor1.adjSpeed(strVal)
                print 'Motor1 t and t1=', str(strVal)
            else:
                print 'failed to parse the a command'
        
        if ret == 'exit':
            return 'im out'
            return Motor1
            
        if ret =='p':
            Motor1.up(steps=1,overrideMaxUp = True)
            #add no logging
        
        if ret =='o':
            Motor1.down(steps=1,overrideMaxDown = True)
        
        if ret =='off':
            Motor1.off()
            
        if ret =='on':
            Motor1.on()
        
        

        
        print str(Motor1.stepInd)
        
    return 'never exit this way' #------------------------------

if __name__=="__main__":    
    #START
    Ser1 = MySerial()
    Motor1 = motorInit(Ser1)

    Motor1.on()
    calibrateMotor(Motor1)

    time.sleep(3)
    Motor1.off()
    time.sleep(3)

    Motor1.on()
    print str(Motor1.stepInd)

    time.sleep(1)
    Motor1.up(steps=400)
    Motor1.up(steps=200)
    Motor1.down(steps=100)
    print str(Motor1.stepInd)

    Motor1.off()
    print str(Motor1.stepInd)

    time.sleep(2)
    Motor1.on()
    print str(Motor1.stepInd)


##EXAMPLE for calibrate phase
    #   Y
    #   on
    #   q 10
    #   w 10
    #   now decide if the direction is correct, if not
    #   reversedir
    
    #   now you go back to motor shell 
    #   motor.off
    #   manually wind to close
    #   wwwwww
    #   w 2
    #   ...
    #   q
    #   setmaxwind   #this sets absolute low


    