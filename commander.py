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
    return pyserialcom.arduisend(msg)

def recordMessage(msg):
    print msg

# return a tuple of r,g,b
def translate(hex_color):
    return (str(int(hex_color[0:2], 16)), str(int(hex_color[2:4], 16)), str(int(hex_color[4:6], 16)))

class Commander():
    def __init__(self):
        self.cmd = 1
        self.state = 'OFF'
        self.ac_state = 'OFF'
        self.iBeaonThreshold = -50
        self.temperature = 0
    def cmdLight(self):
        self.cmd = 1
    def cmdTemp(self):
        self.cmd = 1
    def turnLightON(self, deviceID):
        print 'Turn on light now'
        if self.state == 'ON':
            return 
        self.state = 'ON'
        sendMessage(deviceID + '011200')
    def turnLightOFF(self, deviceID):
        print 'Turn off light now'
        if self.state == 'OFF':
            return 
        self.state = 'OFF'
        sendMessage(deviceID + '010000')   
    def turnACON(self, deviceID):
        print 'Turn AC ON'
        if self.ac_state == 'ON':
            return 
        self.ac_state = 'ON'
        sendMessage(deviceID + '021000')  

    def turnACOFF(self, deviceID):
        print 'Turn AC OFF'
        if self.ac_state == 'OFF':
            return 
        self.ac_state = 'OFF'
        sendMessage(deviceID + '020000')

    def addTemperture(self, deviceID, temperature):
        print 'setTemperture' + str(temperature)
        sendMessage(deviceID + '024000')        

    def decTemperture(self, deviceID, temperature):
        print 'setTemperture' + str(temperature)
        sendMessage(deviceID + '025000')        


    def parseCmd(self, device, cmd):
    	js = json.loads(cmd)
        #print json.dumps(js)
        #print js['a']
        	#print js.has_key('a')
        pyserialcom.arduiinit()
        if device == 'iBeacon':
            for key in js:
                if str(key) == 'rssi':
                    if int(js[key]) >= self.iBeaonThreshold:
                        self.turnLightOn('2351')
                if str(key) == 'ON':
                    if str(js[key]) == 'true' or str(js[key]) == 'True':
                        if self.state == 'ON':
                            return      
                        #self.turnACON('2466')
                        #time.sleep(2)                        
                        #self.addTemperture('2466', str(js[key]))
                        #time.sleep(2)
                        self.turnLightON('2998')

                    if str(js[key]) == 'false' or str(js[key]) == 'False':
                        if self.state == 'OFF':
                            return 
                        self.turnLightOFF('2998')

        elif device == 'ac':
            print "ac json get"
            #pyserialcom.arduiinit()
            deviceID = '2466'
            for key in js:
                if str(key) == 'ON':
                    if str(js[key]) == 'true' or str(js[key]) == 'True':
                        self.turnACON(deviceID)
                        
                    if str(js[key]) == 'false' or str(js[key]) == 'False':
                        self.turnACOFF(deviceID)

                if str(key) == 'Temperature':
                    if str(js[key]) == '-1':
                        continue
                    if int(js[key]) >= int(self.temperature):
                        self.addTemperture(deviceID, str(js[key]))
                    else:
                        self.decTemperture(deviceID, str(js[key]))
                    self.temperature = str(js[key])

                    


        elif device == 'light':
            print "light json get"

            #pyserialcom.arduiinit()
            deviceID = '2998'
            for key in js:
                if str(key) == 'ON':
                    print 'light in key ON'
                    if str(js[key]) == 'true' or str(js[key]) == 'True':
                        self.turnLightON(deviceID)
                    
                    if str(js[key]) == 'false' or str(js[key]) == 'False':
                        self.turnLightOFF(deviceID)
                    

                if str(key) == 'color':
                    if str(js[key]) == 'ffffff':
                        continue
                    rgb_tuple = translate(js[key])
                    c = [0 ,0 ,0]
                    c[0] = rgb_tuple[0]
                    c[1] = rgb_tuple[1]
                    c[2] = rgb_tuple[2]
                    for i in range(0, 3):
                        print i, 'ttttt'
                        if len(c[i]) == 1:
                            c[i] = '00' + c[i]
                        if len(c[i]) == 2:
                            c[i] = '0' + c[i]
                    print 'ttttt'

                    changecolor(deviceID, c[0], c[1], c[2])
            
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





