import serial
import os,sys
import random, time

# 1. Check serial write speed
def logIt(**kwargs):
    
    if not(kwargs.get('output',False)):
        listLog = []
        for i in range(100):
            listLog.append(str(random.random()))
    else:
        output = kwargs.get('output',False)
    
    output = "\n".join(output)
    
    outnum = str(kwargs.get('outnum',int(random.uniform(0,1000))))
    outfile = "out" + outnum + ".txt"
    print outfile
    
    f = open(outfile,'w')
    f.writelines(output)
    f.close()
    
    
#dummy()

def gpioapi(pinNum, command):
        return "gpio " + str(command) + " " + str(pinNum) +  "\r"

class MySerial:
    
    def __init__(self,**kwargs):
        
        portName = kwargs.get('portname','COM3')
        timeOut = kwargs.get('timeout',1.0)
        baud = kwargs.get('baud',19200)
        self.serPort = serial.Serial(portName, baud, timeout=timeOut)
        
        self.thatPin = kwargs.get('thatpin',5)
        
    def test(self,**kwargs):
        """ return info about the serial-port comm """
        return 'idk'
    
    def writeUp(self):
        self.serPort.write(gpioapi(self.thatPin,'set'))
    def writeDown(self):
        self.serPort.write(gpioapi(self.thatPin,'clear'))

def testSerGILInterval(InpSer,**kwargs):
    
    trials = kwargs.get('trials',100)
    sleepy = kwargs.get('sleepy',0)
    
    #Test Serial Write Time
    fLog = []
    for i in range(trials):
        before = time.time()
        
        if i % 2 == 0:
            InpSer.writeDown()
        else:
            InpSer.writeUp()
        
        fLog.append(time.time() - before)
        
        if sleepy > 0:
            time.sleep(sleepy)
            
    if kwargs.get('msunits',False):
        fLog = map(lambda f: float(f * 1000), fLog)
    sLog = map(lambda f: str(f) ,fLog)
    logIt(output=sLog)
    
    if kwargs.get('gap',False):
        biggers = filter(lambda tup: tup[1] > 0, [(i,v) for i,v in enumerate(fLog)])
        
        #print biggers
        
        intervals = map(lambda i: biggers[i+1][0] - biggers[i][0]  ,range(len(biggers)-1))
        print intervals
    
    #Test Avg non-write loop time
    loopLog = []
    before = time.time()
    for i in range(100):
        loopLog.append(time.time() - before)
        before = time.time()
    avgLoopTime = float(sum(loopLog)) / float(len(loopLog))
    print 'avgLoopTime: ', str(avgLoopTime)
    
    numtrials = float(len(fLog))
    print "numtrials: ",str(numtrials)
    sumtrials  = float(sum(fLog))
    avgtime = sumtrials / numtrials
    print "avgWriteTime: ", str(avgtime)
    if kwargs.get('msunits',False):
        print '                    in ms'

    
if __name__ == "__main__":
    
    MySer = MySerial(timeout = .1 ,baud=15200) 
    
    ss = float(float(1)/float(1000))
    
    testSerGILInterval(MySer,msunits=True,trials = 100,gap=True,sleepy = ss)
    
    
# 1. Check if joy2motor works when serPort.serPort.write is used
#    1b. check if try/except gets us 20% there?

# 2. test write speed of 
#    2b. test write speed of gpio set vs. adc read
    
# Get time finer resolution for time, currently 3 decimal places

#Every 33 (sometimes 32 or 34) serial writes has a 15ms (14-16) delay


#Is this occuring on an "800 loop" on the motor?