import sys
import time
import serial

from imports.Motor import Motor as Motor
from imports.Motor import MySerial as MySerial

## Testing ###########################################
def Demo():        
    Ser1 = MySerial()
    
    Motor1 = Motor(Ser1)
    Motor1.on()
    Motor1.wind(steps = 10)

    time.sleep(3)
    Motor1.off()
    time.sleep(3)

    Motor2 = Motor(Ser1)
    Motor2.on()
    Motor2.wind(steps = 400, sleep = .00025)
    time.sleep(3)
    Motor2.off()
    return 1
    
Demo()


