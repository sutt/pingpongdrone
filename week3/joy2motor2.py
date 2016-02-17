import sys
import serial
import time
import thread
import threading
import math

import steering 
from imports.Motor import Motor as Motor
from imports.Motor import MySerial as MySerial    

joy = 500
poll_delay = .1 #.05
actuate_delay = .2 #.05
read_duration = 8 * 4

pollHz = 6
gAccel = 0
gPos = 500

#class Joystick(threading.Thread):
class Joystick:
    def __init__(self,serPortHandle,**kwargs):
        self.serPort = serPortHandle.serPort   #this is .Serial
        #self.lockme = kwargs.get('lockme',False)
        self.lockme=True
        if self.lockme:
            self.lock = threading.Lock()
        else:
            self.lock = None
        self.lockmeread = kwargs.get('lockmeread',False)
        
        
    def writeit(self):
        if self.lockme:
            self.lock.acquire()
        try:
            analogChannel = 4  
            
            self.serPort.write("adc read "+ str(analogChannel) + "\r")
        except:
            print 'joystick-write-err'
        finally:
            if self.lockme:
                self.lock.release()
        return 1
                
    def readit(self):
        if self.lockmeread:
            self.lock.acquire()
        try:
            ret = self.serPort.read(read_duration)
        except:
            print 'joystick-read-err'
            ret = 'read-err'
        finally:
            if self.lockmeread:
                self.lock.release()
        return ret
    
    def hello(self):
        print 'world'

def actuateMotor(accel, mMotor):
    
    entryTime = time.time()
    
    actuateInterval = 1.0 / float(pollHz)
    
    #This is half the period time "on, off, on"
    # 0-500 -> 1-> .00025
    accelPeriod = 1.0 / float(1+(8*accel))  
    
    intervalSteps = int(actuateInterval / accelPeriod)
    modInterval =  actuateInterval % accelPeriod 
    
    if accel > 0:
        mMotor.up(steps = intervalSteps, t = accelPeriod)
        time.sleep(modInterval)
    elif accel < 0:
        mMotor.down(steps = intervalSteps, t = accelPeriod)
        time.sleep(modInterval)
    elif accel == 0:
        time.sleep(actuateInterval)
        
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

def actuate(Ser1):
    
    #Init Motor
    iniMotor = motorInit(Ser1)
    gMotor = steering.calibrateMotor(iniMotor)
    
    while True:
        #print ['down','up'][int(gPos > 500)], str(gAccel - 500)
        #print "gPos:", str(gPos)
        #print "gAccel: ", str(gAccel)
        
        try:
            actuateMotor(gAccel,gMotor)
            time.sleep(.01)
        except:
            print 'motor-err'
        
        #pass
        
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

    serPort = JoyObj.serPort
    global gAccel
    analogChannel = 4  

    while True:
        
        etime = time.time()
        
        try:
            JoyObj.writeit()
            ret = JoyObj.readit()
        except:
            ret = "poll err"
        
        #print ret
        gAccel = setAccel(ret)
        #print gAccel
        
        poll_delay = (1.0 / float(pollHz)) - (time.time() - etime)
        if poll_delay > 0:
            time.sleep(poll_delay)
        #return time.time() - etime
        
    return 1

    
myserial = MySerial(timeout = .05)

Joy = Joystick(myserial)

t1 = threading.Thread(target=poll, args = (Joy,))  #lockme=True,
t1.start()

#t2 = threading.Thread(target=actuate, args = (myserial,))
#t2.start()