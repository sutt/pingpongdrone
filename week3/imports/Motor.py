import sys
import serial
import time
    
    
def gpioapi(pinNum, command):
        return "gpio " + str(command) + " " + str(pinNum) +  "\r"

class MySerial:
    
    def __init__(self,**kwargs):
        
        portName = kwargs.get('portname','COM3')
        timeOut = kwargs.get('timeout',1.0)
        self.serPort = serial.Serial(portName, 19200, timeout=timeOut)
        
    def test(self,**kwargs):
        """ return info about the serial-port comm """
        return 'idk'

class Motor:

    def __init__(self,Ser,**kwargs):
    
        self.globalSer = Ser
        self.serPort = Ser.serPort
    
        self.sleepPin = kwargs.get('sleepPin',3)
        self.dirPin = kwargs.get('dirPin',1)
        self.stepPin = kwargs.get('stepPin',2)

        self.maxWind = kwargs.get('maxWind', 10)
        self.t = .00025
        self.t1 = .00025
        
        self.windDir = kwargs.get('windDir',0)
        self.stepInd = 0     #steps up from baseline 0
        self.stepInd2 = None    #count steps in case x
        self.maxUp = 99999       #how many steps to hit total release
        
        self.log1 = []
        self.log2 = []
        
        
    def on(self,**kwargs):
        self.serPort.write(gpioapi(self.sleepPin, 'set' ))
        return 1
        
    def off(self,**kwargs):
        self.serPort.write(gpioapi(self.sleepPin, 'clear' ))
        self.serPort.write(gpioapi(self.dirPin, 'clear' ))
        self.serPort.write(gpioapi(self.stepPin, 'clear' ))
        return 1
        
    def setWindDir(self,dir):
        self.windDir = dir  # 0 or 1
        return dir
        
    def setDir(self,dir,**kwargs):
        cmd = ['clear', 'set'][dir]
        self.serPort.write(gpioapi(self.dirPin, cmd ))
        return 1
        
    def setWindMax(self):
        self.stepInd = 0
        
    def setReleaseMax(self):
        self.maxUp = self.stepInd
    
    def wind(self,**kwargs):
        steps = kwargs.get('steps',50)
        steps = min(steps,self.maxWind)
        secs = float(kwargs.get('sleep',self.t1))
        self.step(steps, secs)
        
    def up(self,**kwargs):
        steps = kwargs.get('steps',1)
        
        if ((steps + self.stepInd) > self.maxUp) and not(kwargs.get('overrideMaxUp',False)):
            steps = self.maxUp - self.stepInd
            print 'only ', str(steps), ' up'
        
        self.setDir(int(-1*(self.windDir-1)))  #opposite of windDir
        
        if kwargs.get('log',False):
            self.logstep(steps = steps, secs = self.t1)
        else:
            self.step(steps = steps, secs = self.t1)
        self.stepInd = steps + self.stepInd
        return 1
        
    def down(self, **kwargs):
        steps = kwargs.get('steps',1)
        if steps > self.stepInd and not(kwargs.get('overrideMaxDown',False)):
            steps = self.stepInd
            print ' only ', str(self.stepInd)
        
        self.setDir(self.windDir)
        
        if kwargs.get('log',False):
            self.logstep(steps = steps, secs = self.t1)
        else:
            self.step(steps = steps, secs = kwargs.get('t', self.t1))

        self.stepInd = self.stepInd - steps
        return 1
        
    def step(self,steps,secs):
        for s in range(steps):
            try:
                self.serPort.write(gpioapi(self.stepPin,'clear'))
                time.sleep(secs)
                self.serPort.write(gpioapi(self.stepPin,'set'))
                time.sleep(secs)
            except:
                print 'motor-step-err'
        return steps
        
    def logstep(self,steps,secs):
        for s in range(steps):
            before = time.time()
            try:
                self.serPort.write(gpioapi(self.stepPin,'clear'))
                time.sleep(secs)
                self.serPort.write(gpioapi(self.stepPin,'set'))
                time.sleep(secs)
                log1.append(time.time() - before)
                log2.append(1)
            except:
                print 'motor-step-err'
                log1.apend(time.time() - before)
                log2.append(0)
        return steps
        
    def outputlog(self,**kwargs):
        str_output = "\n".join(self.log1)
        print str_output
        return 1

    def gotoBottom(self, **kwargs):
        self.down(steps = self.stepInd, secs = self.t)
        return 1
    