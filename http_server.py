#!/usr/bin/python

"""
Save this file as server.py
>>> python server.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python server.py
Serving on localhost:8000

You can use this to test GET and POST methods.

"""

import SimpleHTTPServer
import SocketServer
import logging
import cgi
import BaseHTTPServer
import sys
import Queue

API_LIGHT = '/api/light'
API_DOOR = 'api/door'
API_AC = 'api/ac'
API_IBEACON = 'api/iBeacon'

def isAPI(API, query):
    return query.find(API) != -1

def toQstr(s):
    return '"' +str(s) + '"'

def getThermostat():
    return True

def getLight():
    return True

def getBrightness():
    return 20

def getColor():
    return '#FFFFFF'

def getHeat():
    return True

def getTemperature():
    return 20

def getLock():
    return True

def getHTTPresponse_get():
    return  '{"Thermostat":' + toQstr(getThermostat()) + \
    ',"Light":'+ toQstr(getLight()) + \
    ',"Brightness":'+ toQstr(getBrightness()) + \
    ',"Color":'+ toQstr(getColor()) + \
    ',"Heat":'+ toQstr(getHeat()) + \
    ',"Temperature":'+ toQstr(getTemperature()) + \
    ',"Lock":'+ toQstr(getLock()) +'}'

def getHTTPresponse_get_light():
    return '{"id":"2998", "ON":"True", "color":"#FFFFFF"}'



class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)

        response = getHTTPresponse_get()
        
        print self.path
        if isAPI(API_LIGHT,self.path):
            print 'Light controll'
            response = getHTTPresponse_get_light()
        elif isAPI(API_DOOR,self.path):
            print 'door controll'

        print response

        #response = 
        self.send_response(200) #create header
        self.send_header("Content-Type", 'application/json')
        self.send_header("Content-Length", len(response))
        self.end_headers()

        self.wfile.write(response) #send response

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        global server_queue
        #logging.warning("======= POST STARTED =======")
        #logging.warning(self.headers)
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        server_queue.put("json_request")
        if isAPI(API_LIGHT,self.path):
            server_queue.put("light")
        elif isAPI(API_DOOR,self.path):
            server_queue.put("door")
        elif isAPI(API_AC, self.path):
            server_queue.put("ac")
        elif isAPI(API_IBEACON, self.path):
            server_queue.put("iBeacon")

        print post_body
        server_queue.put(post_body)
        logging.warning(post_body)
        response = u'{"a":"This is the respon"}'
        #response = 
        self.send_response(200) #create header
        self.send_header("Content-Type", 'application/json')
        self.send_header("Content-Length", len(response))
        self.end_headers()

        self.wfile.write(response) #send response
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

'''
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        logging.warning(post_body);
    logging.warning(post_body);

        logging.warning("======= POST VALUES =======")
        for item in form.list:
            logging.warning(item)
        logging.warning("\n")

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
'''

class HttpServer():
    
    def __init__(self, queue):
        global server_queue
        server_queue = queue
        self.PORT = 8000
        server_queue.put('HTTP port: ' + str(self.PORT))
        self.Handler = ServerHandler
        self.httpd = BaseHTTPServer.HTTPServer(("", self.PORT), self.Handler)

    def loop(self):
        self.httpd.serve_forever(0.5)

    def halt(self):
        self.httpd.shutdown()

'''
def main():
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])
        I = sys.argv[1]
    elif len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        I = ""
    else:
        PORT = 8004
        I = ""
    queue = Queue.Queue()
    Handler = ServerHandler
    httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
    print "@rochacbruno Python http server version 0.1 (for testing purposes only)"
    print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
    keep_running = 1
    while keep_running:
        httpd.handle_request()


if __name__ == '__main__':
    main()
'''