from socket import *
from select import *
import sys
import Queue
import threading

class SocketReceiver:
    def __init__(self, queue):
        self.queue = queue
        self.host = ''
        self.port = 50006
        self.queue.put('Socket port: ' + str(self.port))
        self.serverObj = socket(AF_INET, SOCK_STREAM)
        self.serverObj.bind((self.host, self.port))
        self.serverObj.listen(5)

    def loop(self):
        global run
        while True:
            infds,outfds,errfds = select([self.serverObj,],[],[],5)   
            if(run == 0):
                print 'close'
                #connection.close()
                self.serverObj.close()
                sys.exit()
                break
            if len(infds) != 0:   
                connection, address = self.serverObj.accept()
                infds_c,outfds_c,errfds_c = select([connection,],[],[],3)
                print 'Server Connected by: ', address
                if len(infds_c) != 0:   
                    buf = connection.recv(8196)   
                    if len(buf) != 0:   
                        print str(buf)
                        self.queue.put(str(buf))
                        connection.send('Echo:' + buf)
                connection.close()

run = 0


def main():
    global run
    run = 1
    queue = Queue.Queue()
    sr = SocketReceiver(queue)
    sckt_thread = threading.Thread(target = sr.loop)
    sckt_thread.start()

if __name__ == '__main__':
    main()
