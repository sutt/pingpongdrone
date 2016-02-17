import serial
import os,sys
import random, time

# 1. Check serial write speed
def dummy():
    
    listLog = []
    for i in range(100):
        listLog.append(random.random())
    
    f = open("out1.txt")
    f.writelines(listLog)
    f.close()
