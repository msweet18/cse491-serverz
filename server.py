#!/usr/bin/env python
<<<<<<< HEAD
#copied from mattyayoh
=======
# -*- coding: utf-8 -*-
>>>>>>> master
import random
import socket
import urlparse
import time
from urlparse import urlparse
from StringIO import StringIO
from wsgiref.validate import validator
from sys import stderr

<<<<<<< HEAD
## My app.py
from app import make_app
##

## Quixhote
# import quixote
# from quixote.demo.altdemo import create_publisher
# p = create_publisher()
##

## Image app
# import quixote
# import imageapp
# imageapp.setup()
# p = imageapp.create_publisher()
##

def handle_connection(conn, port):
    """Takes a socket connection, and serves a WSGI app over it.
        Connection is closed when app is served."""
    
    # Start reading in data from the connection
    req = conn.recv(1)
    count = 0
    env = {}
    while req[-4:] != '\r\n\r\n':
        new = conn.recv(1)
        if new == '':
            return
        else:
            req += new

    # Parse the headers we've received
    req, data = req.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        key, val = line.split(': ', 1)
        headers[key.lower()] = val

    # Parse the path and related env info
    urlInfo = urlparse(req.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = urlInfo[2]
    env['QUERY_STRING'] = urlInfo[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = str(0)
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = socket.getfqdn()
    env['SERVER_PORT'] = str(port)
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = stderr
    env['wsgi.multithread']  = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once']     = False
    env['wsgi.url_scheme'] = 'http'
    env['HTTP_COOKIE'] = headers['cookie'] if 'cookie' in headers.keys() else ''

    # Start response function for WSGI interface
    def start_response(status, response_headers):
        """Send the initial HTTP header, with status code 
            and any other provided headers"""
        
        # Send HTTP status
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')

        # Send the response headers
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')
    
    # If we received a POST request, collect the rest of the data
    content = ''
    if req.startswith('POST '):
        # Set up extra env variables
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = str(headers['content-length'])
        env['CONTENT_TYPE'] = headers['content-type']
        # Continue receiving content up to content-length
        cLen = int(headers['content-length'])
        while len(content) < cLen:
            content += conn.recv(1)
        
    # Set up a StringIO to mimic stdin for the FieldStorage in the app
    env['wsgi.input'] = StringIO(content)
    
    # Get the application

    ## My app.py
    wsgi_app = make_app()
    ## 
    
    ## Quixote alt.demo
    # wsgi_app = quixote.get_wsgi_app()
    ##

    ## Imageapp
    # wsgi_app = quixote.get_wsgi_app()
    ##

    ## VALIDATION ##
    wsgi_app = validator(wsgi_app)
    ## VALIDATION ##

    result = wsgi_app(env, start_response)

    # Serve the processed data
    for data in result:
        conn.send(data)

    # Close the connection; we're done here
    conn.close()

def main():
    """Waits for a connection, then serves a WSGI app using handle_connection"""
    # Create a socket object
    sock = socket.socket()
    
    # Get local machine name (fully qualified domain name)
    host = socket.getfqdn()

    # Bind to a (random) port
    # port = random.randint(8000, 9999)
    port = 8088
    sock.bind((host, port))

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    # Now wait for client connection.
    sock.listen(5)

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        conn, (client_host, client_port) = sock.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(conn, client_port)
        
# boilerplate
if __name__ == "__main__":
=======
def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000,9000)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        handle_connection(c)

def handle_connection(conn):
    requestInfo = conn.recv(1024)
    print requestInfo
    requestSplit = requestInfo.split('\r\n')[0].split(' ')
    requestType = requestSplit[0]

    try:
        parsed_url = urlparse.urlparse(requestSplit[1])
        path = parsed_url[2]
    except:
        path = "/404"

    if requestType == "GET":
        if path == '/':
            handle_index(conn)
        elif path == '/content':
            handle_content(conn)
        elif path == '/file':
            handle_file(conn)
        elif path == '/image':
            handle_image(conn)
        elif path == '/submit':
            handle_submit(conn,parsed_url[4])
        else:
            handle_fail(conn)

    elif requestType == "POST":
        if path == '/':
            handle_index(conn)
        elif path == '/submit':
            handle_submit(conn,requestInfo.split('\r\n')[-1])

    else:
        print "ERROR: Invalid Request Made"

    conn.close()

def handle_index(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "<a href='/content'>Content</a><br>" + \
            "<a href='/file'>File</a><br>" + \
            "<a href='/image'>Image</a><br><br>" + \
            "<p><u>Form Submission via GET</u></p>"
            "<form action='/submit' method='GET'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>" + \
            "<p><u>Form Submission via POST</u></p>"
            "<form action='/submit' method='POST'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>")

def handle_submit(conn, args):
    args = args.split("&")

    firstname = args[0].split("=")[1]
    lastname = args[1].split("=")[1]

    conn.send('HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n' + \
              "Hello Mr. %s %s." % (firstname, lastname))


def handle_content(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s Some Content</h1>')
    conn.send('This is Msweet18\'s Web server.')

def handle_file(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s a File</h1>')
    conn.send('This is Msweet18\'s Web server.')

def handle_image(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>Here\'s an Image</h1>')
    conn.send('This is Msweet18\'s Web server.')

def handle_fail(conn, args):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
    conn.send('<h1>You made a bad request :(</h1>')
    conn.send('This is Msweet18\'s Web server.')

if __name__ == '__main__':
>>>>>>> master
    main()
