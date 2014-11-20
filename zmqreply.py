import zmq
import sys
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
        )[20:24])

class MessageReceiver:
    def __init__(self, queue, netport, portnumber):
        global run
        self.wlan_ip = get_ip_address(netport)
        self.port = portnumber
        self.queue = queue
        print self.wlan_ip, ": ", self.port
        #self.queue.put("IP: " +self.wlan_ip + ": " + self.port)
        self.queue.put("IP: " +self.wlan_ip)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        #self.socket.bind("tcp://127.0.0.1:5557")
        print "tcp://%s:%s" % ("*", self.port)
        self.socket.bind("tcp://%s:%s" % ("*", self.port))
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def loop(self):
        global run
        while True: 
            if(run == 0):
                break
            socks = dict(self.poller.poll(1000))
            if socks:
                if socks.get(self.socket) == zmq.POLLIN:
                    message = self.socket.recv(zmq.NOBLOCK)
                    print "got message ",message
                    self.queue.put(message)
            '''
            message = self.socket.recv()
            if(message ==  "show_text"):
                print("Show Text")
                #display.showText()
            elif(message == "show_picture"):
                print("Show Picture")
            elif(message == "play_music"):
                print("Play Music")
                #display.playMusic()
            elif(message == "pause_music"):
                print("Pause Music")
                #display.pauseMusic()
            print "timeout"
            #self.queue.put(message)
            #self.socket.send("Message from %s" % (self.port))
            '''
run = 0