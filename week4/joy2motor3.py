import sys
import serial
import time
import thread
import threading
import math

import calibrate  #.Shell as Shell
from imports.Motor import Motor2 as Motor
from imports.Motor import MySerial as MySerial    
from imports.Motor import MySerialLock as MySerialLock
    
joy = 500
poll_delay = .1 #.05
actuate_delay = .2 #.05
read_duration = 8 * 4

iniTime = time.time()

pollHz = 4
gAccel = 0
gPos = 500

#class Joystick(threading.Thread):
class Joystick:
    def __init__(self,serPortHandle,**kwargs):
        self.serPort = serPortHandle   #this is .Serial
        
        
    def writeit(self):
        
        try:
            analogChannel = 4  
            cmd = "adc read " + str(analogChannel) + "\r"
            self.serPort.writeSer(cmd,lock=True)
        except:
            print 'joystick-write-err'
        
        return 1
                
    def readit(self):
        
        try:
            ret = self.serPort.readSer(read_duration,lock=False)
        except:
            print 'joystick-read-err'
            ret = 'read-err'
        return ret
    
    def acquireLock(self):
        self.serPort.acquireLock()
        return 1
        
    def releaseLock(self):
        self.serPort.releaseLock()
        return 1
    
    def doJoy(self):
        return self.serPort.doJoy(lock=True)
        
    
    def hello(self):
        print 'world'

def actuateMotor(accel, mMotor):
    
    entryTime = time.time()
    
    actuateInterval = 1.0 / float(pollHz)
    
    #This is half the period time "on, off, on"
    # 0-500 -> 1-> .00025
    #accelPeriod = 1.0 / float(1+(8*accel))  
    #intervalSteps = int(actuateInterval / accelPeriod)
    #modInterval =  actuateInterval % accelPeriod 
    
    #intervalSteps = 40
    accelPeriod = .005
    epsilon = float((.001 * 8 * 4) + .01)  #polling locks serial
    epsilon = 0.1
    intervalSteps = int(float(actuateInterval - epsilon) / float(accelPeriod*2))
    #intervalSteps = 20
    #print 'intervalSteps', str(intervalSteps)
    
    try:
        if accel > 0:
            mMotor.up(steps = intervalSteps, t = accelPeriod)
            modInterval = actuateInterval - (time.time() - entryTime) 
            if modInterval < 0:
                print 'LAG up', str(modInterval)
            else:
                print 'ahead up', str(modInterval)
                time.sleep(modInterval)
                
        elif accel < 0:
            #print 'downing'
            mMotor.down(steps = intervalSteps, t = accelPeriod, \
            overrideMaxDown=False)
            modInterval = actuateInterval - (time.time() - entryTime)
            if modInterval < 0:
                print 'LAG down', str(modInterval)
            else:
                print 'ahead down', str(modInterval)
                time.sleep(modInterval)
            
        elif accel == 0:
            time.sleep(actuateInterval)
    except:
        print 'actuateMotor err'
    return time.time() - entryTime

# helpers ----------------------------------
def pause(dispTxt, breaker):
    while(True):
        inp = raw_input(dispTxt)
        if any(keywords in inp for keywords in breaker):
            return inp
    
def motorInit(Ser):
    """ this sets up motor from class """
    pause('Y to continue ...', ['Y'])
    MyMotor = Motor(Ser)
    MyMotor.on()
    return MyMotor
# ------------------------------------------------

def actuate(mMotor, **kwargs):
    
    while True:
        #print ['down','up'][int(gPos > 500)], str(gAccel - 500)
        #print "gPos:", str(gPos)
        #print "gAccel: ", str(gAccel)
        
        try:
            if kwargs.get('log',False):
                print "Actuate gAccel: ", str(gAccel)
            actuateMotor(gAccel,mMotor)
            
            #print "Actuate: ", str(time.time() - iniTime)
            
        except:
            print 'motor-actuate-err'

        
def setAccel(line):
    
    """if poll returns an unreadable line, return the 
    accel of previuos succesful poll"""
    global gPos
    
    try:
        line = line[12:-3]
        iPos = int(line)
    except:
        iPos = gPos
    
    gPos = iPos
    
    if abs(iPos - 500) > 10:
        accel = iPos - 500
    else:
        accel = 0
    return accel
        
        
def poll(JoyObj,**kwargs): 

    global gAccel

    while True:
        
        etime = time.time()
        
        try:
            #JoyObj.acquireLock()
            #JoyObj.writeit()
            #ret = JoyObj.readit()
            #JoyObj.releaseLock()
            ret = JoyObj.doJoy()
        except:
            ret = "poll err"
        
        #print 'POLL ret: ', str(ret)
        #print '~~/ret'
        gAccel = setAccel(ret)
        #print 'poll gAccel: ', str(gAccel)
        
        poll_delay = (1.0 / float(pollHz)) - (time.time() - etime)
        if poll_delay > 0:
            time.sleep(poll_delay)
        #return time.time() - etime
        
        #print "Poll: ", str(time.time() - iniTime)
        
    return 1


def gpioapi(pinNum, command):
        return "gpio " + str(command) + " " + str(pinNum) +  "\r"

        
        
### MAIN -----
if __name__ == "__main__":

    myserial = MySerialLock(timeout = .05)

    myserial.serPort.write(gpioapi(4,'set'))
    Joy = Joystick(myserial)

    #Calibrate Phase...
    mMotor = calibrate.motorInit(myserial)
    calibrate.calibrateMotor(mMotor)
    print 'done calibing'

    #Interactive Mode
    t1 = threading.Thread(target=poll, args = (Joy,))  #lockme=True,
    t1.start()

    t2 = threading.Thread(target=actuate, args = (mMotor,))
    t2.start()
    
    #t3 = threading.ThreaD(target=shell,args = (mMotor,Joy))




