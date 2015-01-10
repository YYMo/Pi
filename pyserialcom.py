#!/usr/bin/python

import serial 
import time
import sys


# test code 
'''
serp = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(1)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 0.1)
time.sleep(1)  
ser.write('1')
time.sleep(0.5)
print("sent stuff to arduino")
print (int(ser.readline()))
time.sleep(0.1)
''' 

# funtions: 

''' 
sending function: 
this function takes in the message to be sent to the arduino
and sends it by establishing serial connection. Returns a 0 
upon success and 1 upon error.
'''  
def arduisend(message):
    print('sending message')
    ser.writelines(message)
    print('message sent')
    time.sleep(2) 
    confirmation = ser.readline()
    print confirmation
    if confirmation == 'got' + message[0:3]:
        return 0
    else:
        return 1

'''
receiving function: arduireceive
this function receives messages from the arduino and returns 
the string received
'''
def arduireceive():
    message = ser.readline()
    time.sleep(0.5)
    print(message) 
    return message
'''
set up function: 
this function acts as the set up function for the connection between
arduino and raspberry pi, needs to be called prior to calling 
the send and receive functions
'''
def arduiinit():
    global serp
    serp = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(1)
    global ser
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 0.1)
    time.sleep(1)

# global variable declaration
serp = 0 
ser = 0 
mess='2991011000'
arduiinit()
arduisend(mess)
arduireceive()


