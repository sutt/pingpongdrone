import sys
import serial
import time
import thread
import threading

joy = 500
poll_delay = .01
actuate_delay = .02


def actuate():
    while True:
        print ['down','up'][int(joy > 500)], str(joy - 500)
        time.sleep(actuate_delay)
    


def poll():
    
    portName = "COM3" #sys.argv[1];
	analogChannel = 4  #sys.argv[2];
    serPort = serial.Serial(portName, 19200, timeout=1)

    while True:
        global joy
        serPort.write("adc read "+ str(analogChannel) + "\r")
        ret = serPort.read(25)
        joy = int(ret)
        print 'poll: ', str(joy)
        time.sleep(poll_delay)

t1 = threading.Thread(target=poll)
t1.start()

t2 = threading.Thread(target=actuate)
t2.start()