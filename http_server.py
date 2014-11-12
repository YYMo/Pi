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

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)

        response = u'{"a":"This is the respon"}'
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
        server_queue.put(str(post_body))
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
        self.PORT = 8004
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