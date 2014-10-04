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
    def __init__(self, queue, portnumber = "10113"):
        self.wlan_ip = get_ip_address('wlan0')
        self.port = portnumber
        self.queue = queue
        print self.wlan_ip, ": ", self.port
        self.queue.put("IP: " +self.wlan_ip + ": " + self.port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://%s:%s" % ("*", self.port))

    def loop(self):
        while True:
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
            self.queue.put(message)
            self.socket.send("Message from %s" % (self.port))


def main():
    port = "10113"
    if len(sys.argv) > 1:
        port = sys.argv[1]
    mr = MessageReceiver(port)
    mr.loop()

if __name__ == '__main__':
    main()
