import sys
import serial
import time
    
portName = "COM3"   

serPort = serial.Serial(portName, 19200, timeout=1)

serPort.write("gpio clear 3" + "\r")
