import sys
import serial
import time
import threading
    
    
def gpioapi(pinNum, command):
        return "gpio " + str(command) + " " + str(pinNum) +  "\r"
        
#logging client
import zmq
#context = zmq.Context()
#print("Connecting to hello world server...")
#socket = context.socket(zmq.REQ)
#socket.connect("tcp://localhost:5555")

port  = 5556
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

def sendMsg(msg):
    sMsg  = "motor: "
    sMsg +=    str(msg)
    #sMsg = "yoMotor"
    try:
        socket.send(sMsg)
    except:
        #print '___motor couldnt send msg', str(sMSg)
        pass
    #message = socket.recv()
    # try:
        # message = socket.recv()
    # except:
        # print '__motro couldnt receive'
    
    return 1

class MySerialLock:
    
    def __init__(self,**kwargs):
        
        portName = kwargs.get('portname','COM7')
        timeOut = kwargs.get('timeout',1.0)
        self.serPort = serial.Serial(portName, 19200, timeout=timeOut)
        self.lock = threading.Lock()
        self.lockread = True
        self.lockwrite = True
        
    def writeSer(self,cmd,**kwargs):
        lock = kwargs.get('lock', self.lockwrite)
        if lock:
            self.lock.acquire()
            #print 'LOCK--------------'
        try:
            #print cmd
            self.serPort.write(cmd)         
        except:
            print 'unable to write: '. str(cmd)
            #self.test() is locked?
        finally:
            if lock:
                self.lock.release()
                #print 'un______________LOCK'
    
    def readSer(self,cmd,**kwargs):
        lock = kwargs.get('lock', self.lockread)
        if lock:
            self.lock.acquire()
            print 'LOCK--------------RRR'
        try:
            read_duration = 8 * 4
            ret = self.serPort.read(read_duration)
        except:
            print 'unable to read: '
            ret = ''
        finally:
            if self.lock:
                self.lock.release()
                print 'RRRun______________LOCK'
        return ret
    
    def doJoy(self,**kwargs):
        lock = kwargs.get('lock', self.lockwrite)
        if lock:
            getLock = True
            while(getLock):
                try:
                    if kwargs.get('logJoy',False):
                        print 'try for it'
                    self.lock.acquire()
                    getLock = False
                except:
                    print 'nah'
                    
            #print 'LOCK--------------joy'
        
        #serial.flush?
        try:
            self.serPort.flushInput()
        except:
            print 'unable to flush joy'
        
        try:
            self.serPort.write("adc read 4\r")         
        except:
            print 'unable to joy write'
        
        try:
            ret = self.serPort.read(8*4)
            if kwargs.get('logJoy',False):
                print 'DOJOY ret: ', ret
                print '~~/ret'
        except:
            print 'unable to joy read'
            ret = 'nope'
        
        if lock:
            self.lock.release()
            #print 'un______________LOCKjoy'

        return ret
    
    def acquireLock(self):
        self.lock.acquire()
        print 'ACQUIRE-------------------'
        return 1
        
    def releaseLock(self):
        self.lock.release()
        print '------------------RELEASE'
    
    def test(self,**kwargs):
        """ return info about the s erial-port comm """
        return 'idk'
        

class MySerial:
    
    def __init__(self,**kwargs):
        
        portName = kwargs.get('portname','COM7')
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

        self.maxWind = kwargs.get('maxWind', 1000)
        self.t = .00025 #.01 #.00025
        self.t1 = .00025 #.01  #.00025
        
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
        
    def adjSpeed(self,input,**kwargs):
        try:
            myt = float(input)
        except:
            print 'adjSpeed error: input was not a float'
            return 0
        if (myt > 0) & (myt < 1.0) or kwargs.get('overSpeed',false):
            self.t = myt
            return 1
        print 'the value of input' , str(input), ' is outside the allowable bounds'
        return 0
    
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
        print 'up'
        steps = kwargs.get('steps',1)
        
        if ((steps + self.stepInd) > self.maxUp) and not(kwargs.get('overrideMaxUp',False)):
            steps = self.maxUp - self.stepInd
            print 'only ', str(steps), ' up'
        
        self.setDir(int(-1*(self.windDir-1)))  #opposite of windDir
        
        _t = kwargs.get('t', self.t1)
        
        
        if kwargs.get('log',False):
            self.logstep(steps = steps, secs = _t)
        else:
            self.step(steps = steps, secs = _t)
            
        self.stepInd = steps + self.stepInd
        return 1
        
    def down(self, **kwargs):
        #print 'down'
        steps = kwargs.get('steps',1)
        if steps > self.stepInd and not(kwargs.get('overrideMaxDown',False)):
            steps = self.stepInd
            print ' only ', str(self.stepInd)
        
        self.setDir(self.windDir)
        
        _t = kwargs.get('t', self.t1)
        
        if kwargs.get('log',False):
            self.logstep(steps = steps, secs = _t)
        else:
            self.step(steps = steps, secs = _t)

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
                self.log1.append(time.time() - before)
                self.log2.append(1)
            except:
                print 'motor-step-err-log'
                self.log1.append(time.time() - before)
                self.log2.append(0)
        return steps
        
    def outputlog(self,**kwargs):
        str_output = map(lambda s: str(s), self.log1)
        str_output = "\n".join(str_output)
        print str_output
        return 1    

    def gotoBottom(self, **kwargs):
        self.down(steps = self.stepInd, secs = self.t)
        return 1
##
        
class Motor2:

    def __init__(self,Ser,**kwargs):
    
        self.globalSer = Ser
        self.serPort = Ser
    
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
        self.serPort.writeSer(gpioapi(self.sleepPin, 'set' ))
        return 1
        
    def off(self,**kwargs):
        self.serPort.writeSer(gpioapi(self.sleepPin, 'clear' ))
        self.serPort.writeSer(gpioapi(self.dirPin, 'clear' ))
        self.serPort.writeSer(gpioapi(self.stepPin, 'clear' ))
        return 1
        
    def adjSpeed(self,input,**kwargs):
        try:
            myt = float(input)
        except:
            print 'adjSpeed error: input was not a float'
            return 0
        if (myt > 0) & (myt < 1.0) or kwargs.get('overSpeed',false):
            self.t = myt
            self.t1 = myt
            return 1
        print 'the value of input' , str(input), ' is outside the allowable bounds'
        return 0
        
    def setWindDir(self,dir):
        self.windDir = dir  # 0 or 1
        return dir
        
    def setDir(self,dir,**kwargs):
        cmd = ['clear', 'set'][dir]
        self.serPort.writeSer(gpioapi(self.dirPin, cmd ))
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
        #print 'up'
        steps = kwargs.get('steps',1)
            
        if ((steps + self.stepInd) > self.maxUp) and not(kwargs.get('overrideMaxUp',False)):
            steps = self.maxUp - self.stepInd
            print 'only ', str(steps), ' up'
        
        self.setDir(int(-1*(self.windDir-1)))  #opposite of windDir
        
        _t = kwargs.get('t', self.t1)
        
        if kwargs.get('log',False):
            self.logstep(steps = steps, secs = _t)
        elif kwargs.get('timeout', 0) > 0:
            ret = self.step(steps = steps, secs = _t, timeout = kwargs.get('timeout', 0))
            if ret < steps:
                steps = ret
        else:
            self.step(steps = steps, secs = _t)
        self.stepInd = self.stepInd + (steps * [-1,1][self.windDir])
        return 1
        
    def down(self, **kwargs):
        steps = kwargs.get('steps',1)
        if steps > self.stepInd and not(kwargs.get('overrideMaxDown',False)):
            steps = self.stepInd
            
            if kwargs.get('zmq',True):
                sendMsg(' only down' + str(self.stepInd))
            else:
                print ' only down', str(self.stepInd)
        
        self.setDir(self.windDir)
        
        _t = kwargs.get('t', self.t1)
        
        if kwargs.get('log',False):
            self.logstep(steps = steps, secs = _t)
        elif kwargs.get('timeout', 0) > 0:
            ret = self.step(steps = steps, secs = _t, timeout = kwargs.get('timeout', 0))
            if ret < steps:
                steps = ret
        else:
            self.step(steps = steps, secs = _t)

        self.stepInd = self.stepInd + (steps * [1,-1][self.windDir])
        return 1
        
    def step(self,steps,secs,**kwargs):
        timeout = kwargs.get('timeout',0)
        for s in range(steps):
            try:
                if timeout > 0:
                    if time.time() > timeout:
                        #print 'cutoff s=', str(s)
                        return s
                
                self.serPort.writeSer(gpioapi(self.stepPin,'clear'))
                time.sleep(secs)
                self.serPort.writeSer(gpioapi(self.stepPin,'set'))
                time.sleep(secs)
            except:
                print 'motor-step-err'
        return steps
        
    def logstep(self,steps,secs):
        print 'logstep'
        for s in range(steps):
            before = time.time()
            try:
                self.serPort.writeSer(gpioapi(self.stepPin,'clear'))
                time.sleep(secs)
                self.serPort.writeSer(gpioapi(self.stepPin,'set'))
                time.sleep(secs)
                self.log1.append(time.time() - before)
                self.log2.append(1)
            except:
                print 'motor-step-err'
                self.log1.append(time.time() - before)
                self.log2.append(0)
        return steps
        
    def outputlog(self,**kwargs):
        str_output = map(lambda s: str(s), self.log1)
        str_output = "\n".join(str_output)
        print str_output
        return 1    

    def gotoBottom(self, **kwargs):
        self.down(steps = self.stepInd, secs = self.t)
        return 1
    