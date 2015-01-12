import json
import pyserialcom

class Commander():
    def __init__(self):
        self.cmd = 1
    def cmdLight(self):
        self.cmd = 1
    def cmdTemp(self):
        self.cmd = 1
    def parseCmd(self, str):
    	js = json.loads(str)
        print json.dumps(js)
        #print js['a']
        	#print js.has_key('a')
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
	cmd = Commander();
	data = '{"a":"b", "c":"d"}'
	cmd.parseCmd(data);
	sample_open_door = '{"lock":"True"}'
	sample_close_door = '{"lock":"False"}'
	cmd.parseCmd(sample_close_door)
	cmd.parseCmd(sample_open_door)

if __name__ == '__main__':
    main()





