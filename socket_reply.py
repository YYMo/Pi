from socket import *

class SocketReceiver:
    def __init__(self, queue):
        self.queue = queue
        self.host = ''
        self.port = 50007
        self.serverObj = socket(AF_INET, SOCK_STREAM)
        self.serverObj.bind((self.host, self.port))
        self.serverObj.listen(5)

    def loop(self):
        global run
        while True:
            connection, address = self.serverObj.accept()
            print 'Server Connected by: ', address
            while True:
                if(run == 0):
                    break
                data = connection.recv(1024)
                if not data: break;
                print str(data)
                print 'socket got data: ', data
                self.queue.put(data)
                connection.send('Echo:' + data)
            connection.close()

run = 0