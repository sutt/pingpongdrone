import sys
import serial
import time

import sys
import time
import serial

from imports.Motor import Motor as Motor
from imports.Motor import MySerial as MySerial    
    
    
## Calibration Program Flow #######################

def pause(dispTxt, breaker):
    while(True):
        inp = raw_input(dispTxt)
        if any(keywors in inp for keywords in breaker):
            return inp
    
def parseQW(cmd):
    """cmd of form <q> <N> or <qqq...q> """
    words = cmd.split(' ')
    if len(words) > 1
        return int(words[1])
    return max( [ words[0].count(s) for s in ["q","w"]] )
    


###Calibration ManualRun #############################    

def motorInit(Ser):
    """ this sets up motor from class """
    pause('Y to continue ...', ['Y'])
    MyMotor = Motor(Ser)
    return MyMotor
    
def calibrateMotor(Motor1):
        
    #Now loop untill configured
    while(True):
        
    ret = pause('q to release, w to wind ...', \
                ['q','w','exit', 'reversedir','setwindmax'])
        
        #respond to input ---------------
        if ret[0] == 'q':
            retsteps = parseQW(ret)
            Motor1.up(steps = retsteps)
            print str(retsteps)
        
        if ret[0] == 'w':
            retsteps = parseQW(ret)
            Motor1.down(steps = retsteps)
            print str(retsteps)
            
        if ret == 'reversedir':
            Motor1.windDir = -1*(Motor1.windDir - 1)
        
        if ret == 'setwindmax':
            Motor1.setWindMax()
            print 'wound, stepind: ', str(Motor1.stepInd)
        
        if ret == 'exit'
            return 'im out'
            
    return 'never exit this way' #------------------------------
    
#START
if __name__=="__main__":

    Ser1 = MySerial()
    Motor1 = initMotor(Ser1)

    Motor1.on()
    calibrateMotor(Motor1)

    time.sleep(3)
    Motor1.off()
    time.sleep(3)

    Motor1.on()
    print str(Motor1.stepInd)

    time.sleep(1)
    Motor1.up(400)
    Motor1.up(200)
    Motor1.down(100)
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


    