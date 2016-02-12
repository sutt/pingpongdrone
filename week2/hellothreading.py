import time
import thread
import random
import threading

def print_time(threadName,delay):
    count = 0
    while count <5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % (threadName, time.ctime(time.time()) )

def basic():    
    try:
        thread.start_new_thread( print_time, ("Thread-1", 2, ) )
        thread.start_new_thread( print_time, ("Thread-2", 4, ) )
    except:
        print 'nah no thread'
        
    while 1:
        pass
        
#basic()

bar = False

def foo():
    counter = 0
    while True:
        if bar == True:
            print 'Success!'
            
        else:
            counter += 1
            print 'nyeet: ', str(counter)
        time.sleep(.01)
    
def example():
    while True:
        global bar
        print 'init'
        time.sleep(5)
        bar = True
        return 'retiring 2'

t1 = threading.Thread(target=foo)
t1.start()

t2 = threading.Thread(target=example)
t2.start()

print 'done'






    