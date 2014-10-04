import threading
import Queue
import guiexample
import zmqreply
from Tkinter import Tk
import musicplayer

class ThreadedClient:
    def __init__(self, parent, netport, portnumber):
        self.queue = Queue.Queue()
        self.parent = parent
        self.musicplayer = musicplayer.MusicPlayer()
        self.gui = guiexample.Example(self.parent, self.queue, self.musicplayer, self.endApplication)
        self.replier = zmqreply.MessageReceiver(self.queue, netport, portnumber)

        self.running = 1
        self.zmqthread = threading.Thread(target = self.replier.loop)
        self.zmqthread.start()

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
            import sys
            print "exit(1)"
            sys.exit(1)
        self.parent.after(200, self.periodicCall)

    def endApplication(self):
        print "endApp"
        self.running = 0




def main():
    port = "10113"
    netport = 'wlan0'
    if len(sys.argv) > 1:
        port = sys.argv[1]
    if len(sys.argv) > 2:
        port = sys.argv[2]
    root = Tk()
    client = ThreadedClient(root, netport, port)
    root.mainloop()  

if __name__ == '__main__':
    main()
