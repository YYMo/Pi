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
    if confirmation == 'sent' + message[0:3]:
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


'''
Colour function: changecolor
Inputs: 
DeviceID: a four digit devide id to send the command to 
Red: the colour of red to display, [0,255] in string 
Green: the colour of green to display, [0,255] in string
Blue: the colour of blue to display, [0,255] in string
Functionality: 
this function makes use of the three functions of 
Output: The output of this function is 0 if all commands are received 
and 1 if one of the messages failed 
Edge Cases
'''
def changecolor(deviceID, Red, Green, Blue):
    red = deviceID + '014' + Red
    green = deviceID + '014' + Green
    blue = deviceID + '014' + Blue

    send_red = arduisend(red)
    send_green = arduisend(green)
    send_blue = arduisend(blue)

    if send_red == 1 and send_green == 1 and send_blue == 1: 
        return 0 
    else: 
        print ('colours not sent')
        return 1 

''' 
Sensor Poll function: pollsensor
this function sends a message and returns the sensor information from 
the arduino sensor 
Inputs: None 
Output: the sensor information 
if failed, returns the value read from serial port
'''
def pollsensor(deviceID):
    mssage = deviceID + '013000'
    arduisend('mssage')
    val = arduireceive()
    return val
