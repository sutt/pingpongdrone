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

pollHz = 60
gAccel = 0
gPos = 500

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
        
        
def poll(serObj,**kwargs): 

    serPort = serObj.serPort
    global gAccel
    #portName = "COM3" 
    analogChannel = 4  
    #serPort = serial.Serial(portName, 19200, timeout=.05)  #or 15200?

    while True:
        
        etime = time.time()
        try:
            serPort.write("adc read "+ str(analogChannel) + "\r")
            ret = serPort.read(read_duration)
        except:
            ret = "err"
        #print ret
        gAccel = setAccel(ret)
        #print gAccel
        
        poll_delay = max(time.time() - etime - (1.0 / float(pollHz)),0)
        
        if poll_delay > 0:
            time.sleep(poll_delay)
        #return time.time() - etime
        
    return 

    
myserial = MySerial(timeout = .05)

t1 = threading.Thread(target=poll, args = (myserial,))
t1.start()

t2 = threading.Thread(target=actuate, args = (myserial,))
t2.start()