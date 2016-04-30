import sys
import zmq

port = 5555
port1 = 5556

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

#from main
socket.connect("tcp://localhost:%s" % port)

#from motor
socket.connect("tcp://localhost:%s" % port1)

socket.setsockopt(zmq.SUBSCRIBE,"")

print 'server setup'

while True:
    print 'in here'
    string = socket.recv()
    print 'not blocked out'
    print string
    
print 'done'

   