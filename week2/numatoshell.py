import sys
import serial

if (len(sys.argv) < 2):
	print "Usage: gpiowrite.py <PORT> <GPIONUM> <COMMAND> \nEg: gpiowrite.py COM1 0 set"
	sys.exit(0)
else:
	portName = sys.argv[1];
	gpioNum = sys.argv[2];
	command = sys.argv[3];

#Open port for communication	
serPort = serial.Serial(portName, 19200, timeout=1)

#Send the command
serPort.write("gpio "+ command +" "+ str(gpioNum) + "\r")

print "Command sent..."
	
#Close the port
serPort.close()