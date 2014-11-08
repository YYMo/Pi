# A simple network chat program between to Raspberry Pi's

import network
import sys
import Queue
'''
def heard(phrase):
  print "them:" + phrase

print "Chat Program"

if (len(sys.argv) >= 2):
  network.call(sys.argv[1], whenHearCall=heard)
else:  
  network.wait(whenHearCall=heard)

print "Chat away!"  
while network.isConnected():
  phrase = raw_input()
  print "me:" + phrase
  network.say(phrase)
'''

class socket_chat:
    def __init__(self, queue, dstIP):
        self.queue = queue
        self.dstIP = dstIP
        network.call(dstIP, whenHearCall=heard)
    
    def send(self, msg):
        network.say(msg);


def main():
    queue = Queue.queue()
    sc = socket_chat(queue, '138.51.207.4')
    sc.send('hello')

if __name__ == '__main__':
    main()



