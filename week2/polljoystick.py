import sys
import serial
import time
import thread
import threading

joy = 500
poll_delay = .1 #.05
actuate_delay = .2 #.05
read_duration = 8

#Why is pySerial so slow? set timeout / eol for read
#http://stackoverflow.com/questions/19908167/reading-serial-data-in-realtime-in-python

#python numatoshell.py COM3 4 set   #this sets IO4 to high for VCC
#now you can read from analog4 which is IO6 (IO4 does not have analog)


def actuate():
    while True:
        #print ['down','up'][int(joy > 500)], str(joy - 500)
        time.sleep(actuate_delay)

def poll(): 

    global joy
    portName = "COM3" 
    analogChannel = 4  
    serPort = serial.Serial(portName, 15200, timeout=.05)

    while True:
        
        try:
            a = time.time()
            serPort.write("adc read "+ str(analogChannel) + "\r")
            #time.sleep(poll_delay)
            
            ret = []
            for i in range(4):
                a = time.time()
                #time.sleep(poll_delay)
                ret.append( (i,serPort.read(read_duration)))
                #ret.append( (i,str(time.time() - a),serPort.read(25)))
            
            print ret
            print str(time.time() - a)
            #print ret[10:-3]
        except:
            'no ret'
        #print 'poll: ', str(ret[10:13])
        #print ret[7:10]
        
        try:
            inter = int(ret[10:-3])
        except:
            inter = 500
        joy = inter
        #time.sleep(poll_delay)

t1 = threading.Thread(target=poll)
t1.start()

t2 = threading.Thread(target=actuate)
t2.start()