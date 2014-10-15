import threading
import Queue
import guiexample
import zmqreply
from Tkinter import Tk
import sys
import musicplayer
import Tkinter
import time

class ThreadedClient:
    
    def __init__(self, parent, netport, portnumber):
        # netport: eth0, wlan

        self.queue = Queue.Queue()
        self.parent = parent
        self.musicplayer = musicplayer.MusicPlayer()
        self.gui = guiexample.Example(self.parent, self.queue, self.musicplayer, self.endApplication)
        self.replier = zmqreply.MessageReceiver(self.queue, netport, portnumber)

        zmqreply.run = 1
        self.zmqthread = threading.Thread(target = self.replier.loop)

        self.zmqthread.start()

        self.running = 1
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            # Doing some clean up work here
            self.parent.quit();
        self.parent.after(300, self.periodicCall)

    def endApplication(self):
        print "endApp"
        self.gui.showPic = 0
        zmqreply.run = 0
        time.sleep(3)
        self.running = 0
        #self.parent.quit();



# argv[1]: portnumber for example: 6700
# argv[2]: netport name for example: eth0, em1, wlan

def main():
        
    port = "10113"
    netport = 'wlan0'
    if len(sys.argv) > 1:
        port = sys.argv[1]
    if len(sys.argv) > 2:
        netport = sys.argv[2]
    root = Tk()
    client = ThreadedClient(root, netport, port)
    #client.endApplication()
    root.mainloop()  

if __name__ == '__main__':
    main()
