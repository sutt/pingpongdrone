import sys
import serial
import time
    
portName = "COM3"   

stepNum = 1
dirNum = 2
sleepNum = 3

numsteps = int(sys.argv[1])
sleepsecs = sys.argv[2]
dir = int(sys.argv[3])


serPort = serial.Serial(portName, 19200, timeout=1)

time.sleep(1)
serPort.write("gpio clear " + str(stepNum) + "\r")
serPort.write("gpio set " + str(sleepNum) + "\r")

serPort.write("gpio " + ["clear ","set "][dir] +  str(dirNum) + "\r")
time.sleep(.2)


for i in range(numsteps):

    serPort.write("gpio set " + str(stepNum) + "\r")
    time.sleep(float(sleepsecs))
    serPort.write("gpio clear " + str(stepNum) + "\r")
    time.sleep(float(sleepsecs))
    print i

print 'done'
time.sleep(1)
serPort.write("gpio clear " + str(sleepNum) + "\r")
print 'released'
serPort.close()

#python hello_numato.py 50 .1 1