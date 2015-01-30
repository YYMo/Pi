import json
import pyserialcom
import time

def changecolor(deviceID, Red, Green, Blue):
    red = deviceID + '014' + str(Red)
    green = deviceID + '015' + str(Green)
    blue = deviceID + '016' + str(Blue)
    r = sendMessage(red)
    time.sleep(2)
    g = sendMessage(green)
    time.sleep(2)
    b = sendMessage(blue)
    time.sleep(2)
    print 'result: ', r, g, b


def sendMessage(msg):
    recordMessage(msg)
    #return pyserialcom.arduisend(msg)

def recordMessage(msg):
    print msg

# return a tuple of r,g,b
def translate(hex_color):
    return (str(int(hex_color[0:2], 16)), str(int(hex_color[2:4], 16)), str(int(hex_color[4:6], 16)))

class Commander():
    def __init__(self):
        self.cmd = 1
        self.state = 'OFF'
        self.iBeaonThreshold = -50
    def cmdLight(self):
        self.cmd = 1
    def cmdTemp(self):
        self.cmd = 1
    def turnLightOn(self, deviceID):
        print 'Turn on light now'
        self.state = 'ON'
        sendMessage(deviceID + '011200')
    def turnLightOff(self, deviceID):
        print 'Turn off light now'
        self.state = 'OFF'
        sendMessage(deviceID + '010000')   
    def setTemperture(self, devicedID, temperature):
        print 'setTemperture' + str(temperature)
        

    def parseCmd(self, device, cmd):
    	js = json.loads(cmd)
        #print json.dumps(js)
        #print js['a']
        	#print js.has_key('a')
        
        if device == 'iBeacon':
            for key in js:
                if str(key) == 'rssi':
                    if int(js[key]) >= self.iBeaonThreshold:
                        self.turnLightOn('2351')


        elif device == 'ac':
            print "ac json get"
            #pyserialcom.arduiinit()
            deviceID = '9999'
            for key in js:
                if str(key) == 'ON':
                    print 'now state:', js[key], self.state
                    if str(js[key]) == 'true' or str(js[key]) == 'True' and self.state == 'OFF':
                        self.turnLightOn(deviceID)
                        
                    if str(js[key]) == 'false' or str(js[key]) == 'False' and self.state == 'ON':
                        self.turnLightOff(deviceID)

                if str(key) == 'temperature':
                    if str(js[key]) == '-1':
                        continue
                    print 'set temperature' + str(js[key])


        elif device == 'light':
            print "light json get"

            #pyserialcom.arduiinit()
            deviceID = '2351'
            for key in js:
                if str(key) == 'ON':
                    print 'now state:', js[key], self.state
                    if str(js[key]) == 'true' or str(js[key]) == 'True' and self.state == 'OFF':
                        turnLightOn(deviceID)
                        
                    if str(js[key]) == 'false' or str(js[key]) == 'False' and self.state == 'ON':
                        turnLightOff(deviceID)
                    

                if str(key) == 'color':
                    if str(js[key]) == 'ffffff':
                        continue
                    rgb_tuple = translate(js[key])
                    changecolor(deviceID, '255', '196', '000')
            
            pyserialcom.arduireceive()

        if js.has_key('Lock'):
        	print 'has lock: ', js['Lock']
        	if js['Lock'] == 'True' or js['Lock'] == 'true':
        		print 'Lock door'
        	if js['Lock'] == 'False' or js['Lock'] == 'false':
        		print 'Open door'
        elif js.has_key('Temperature'):
        	print 'Set Temperature'
        elif js.has_key('Color'):
            print 'Set Color'





def main():
    print 'ha'

if __name__ == '__main__':
    main()





