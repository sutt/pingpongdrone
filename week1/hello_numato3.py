import sys
import serial
import time
    
portName = "COM3"   

stepNum = 2
dirNum = 2
sleepNum = 3

numsteps = int(sys.argv[1])
sleepsecs = sys.argv[2]
dir = int(sys.argv[3])
print numsteps, sleepsecs, dir

serPort = serial.Serial(portName, 19200, timeout=1)
#serPort.write("gpio set" + str(sleepNum) + "\r")

serPort.close()

#python hello_numato.py 50 .1 1