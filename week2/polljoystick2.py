import sys
import serial
import time
import thread
import threading
import math

joy = 500
poll_delay = .1 #.05
actuate_delay = .2 #.05
read_duration = 8

#Why is pySerial so slow? set timeout / eol for read
#http://stackoverflow.com/questions/19908167/reading-serial-data-in-realtime-in-python

#python numatoshell.py COM3 4 set   #this sets IO4 to high for VCC
#now you can read from analog4 which is IO6 (IO4 does not have analog)

#use Queue to share data between threads
#http://stackoverflow.com/questions/16044452/sharing-data-between-threads-in-python

pollHz = 60
gAccel = 0
gPos = 500

def actuateMotor(accel, mMotor):
    
    entryTime = time.time()
    
    actuateInterval = 1.0 / float(pollHz)
    
    #This is half the period time "on, off, on"
    # 0-500 -> 1-> .00025
    accelPeriod = 1.0 / float(1+(8*accell))  
    
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


def actuate():
    
    global gAccel
    
    #Init Motor
    Ser1 = MySerial()
    gMotor = Motor(Ser1)
    
    while True:
        #print ['down','up'][int(joy > 500)], str(joy - 500)
        actuateMotor(gAccel,gMotor)
    
        
def setAccel(line):
    
    """if poll returns an unreadable line, return the 
    accel of previuos succesful poll"""
    global gPos
    
    try:
        iPos = int(line)
    except:
        iPos = gPos
    
    gPos = iPos
    
    if abs(iPos - 500) > 10:
        accel = iPos - 500
    else:
        accel = 0
    return accel
        
        
def poll(**kwargs): 

    global gAccell
    portName = "COM4" 
    analogChannel = 4  
    serPort = serial.Serial(portName, 19200, timeout=.05)  #or 15200?

    while True:
        
        etime = time.time()
        try:
            serPort.write("adc read "+ str(analogChannel) + "\r")
            ret = serPort.read(read_duration)
        except:
            ret = "err"
        
        gAccel = setAccel(ret)
        
        poll_delay = math.max(time.time() - etime - (1.0 / float(pollHz)),0)
        if poll_delay > 0:
            time.sleep(poll_delay)
        #return time.time() - etime
        
    return 

t1 = threading.Thread(target=poll)
t1.start()

t2 = threading.Thread(target=actuate)
t2.start()