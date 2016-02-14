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

def actuate():
    while True:
        #print ['down','up'][int(joy > 500)], str(joy - 500)
        time.sleep(actuate_delay)

def poll(**kwargs): 

    global joy
    portName = "COM4" 
    analogChannel = 4  
    serPort = serial.Serial(portName, 19200, timeout=.05)  #or 15200?

    while True:
        
        etime = time.time()
        try:
            serPort.write("adc read "+ str(analogChannel) + "\r")
            ret = serPort.read(read_duration)
            print ret[12:-3]
        except:
            print 'no ret'
        joy = inter
        poll_delay = math.max(time.time() - etime - (1.0 / float(pollHz)),0)
        if poll_delay > 0:
            time.sleep(poll_delay)
        
        return 

t1 = threading.Thread(target=poll)
t1.start()

t2 = threading.Thread(target=actuate)
t2.start()