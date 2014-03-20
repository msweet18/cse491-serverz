import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

<<<<<<< HEAD
def test_handle_connection_slash():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_get_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_404():
    conn = FakeConnection("GET /asdf HTTP/1.0\r\n\r\n")
    er = 'HTTP/1.0 404 Not Found\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_submit_get():
    fname = "Ben"
    lname = "Taylor"
    conn = FakeConnection("GET /submit?firstname={0}&lastname={1} \
                           HTTP/1.0\r\n\r\n".format(fname, lname))
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)  

def test_submit_post_urlencoded():
    fname = "Ben"
    lname = "Taylor"
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                           "Content-Length: 29\r\n" + \
                           "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                           "firstname={0}&lastname={1}\r\n".format(fname, lname))
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_multipart():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 374\r\n" + \
                          "Content-Type: multipart/form-data; " + \
                          "boundary=32452685f36942178a5f36fd94e34b63\r\n\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63\r\n" + \
                          "Content-Disposition: form-data; name=\"lastname\";" + \
                          " filename=\"lastname\"\r\n\r\n" + \
                          "taylor\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63\r\n" + \
                          "Content-Disposition: form-data; name=\"firstname\";" + \
                          " filename=\"firstname\"\r\n\r\n" + \
                          "ben\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63\r\n" + \
                          "Content-Disposition: form-data; name=\"key\";" + \
                          " filename=\"key\"\r\n\r\n" + \
                          "value\r\n" + \
                          "--32452685f36942178a5f36fd94e34b63--\r\n"
                    )
    fname = 'ben'
    lname = 'taylor'
    er = 'HTTP/1.0 200 OK\r\n'

    server.handle_connection(conn, 80)

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_404():
    conn = FakeConnection("POST /asdf HTTP/1.0\r\n" + \
                          "Content-Length: 0\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
                         )
    server.handle_connection(conn, 80)

    er = 'HTTP/1.0 404 Not Found\r\n'

    assert conn.sent[:len(er)] == er, 'Got: %s' % (repr(conn.sent),)
=======
# Test a basic GET call.

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here\'s Some Content</h1>' + \
                      'This is Msweet18\'s Web server.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here\'s a File</h1>' + \
                      'This is Msweet18\'s Web server.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Here\'s an Image</h1>' + \
                      'This is Msweet18\'s Web server.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_fail():
    conn = FakeConnection("GET /fail HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>You made a bad request :(</h1>' + \
                      'This is Msweet18\'s Web server.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "<a href='/content'>Content</a><br>" + \
                      "<a href='/file'>File</a><br>" + \
                      "<a href='/image'>Image</a><br><br>" + \
                      "<p><u>Form Submission via GET</u></p>" + \
                      "<form action='/submit' method='GET'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>" + \
                      "<p><u>Form Submission via POST</u></p>" +\
                      "<form action='/submit' method='POST'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>"

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit():
    conn = FakeConnection("GET /submit?firstname=Max&lastname=Sweet HTTP/1.1\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Mr. Max Sweet."

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


# Post Tests --------

def test_handle_post_index():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "<a href='/content'>Content</a><br>" + \
                      "<a href='/file'>File</a><br>" + \
                      "<a href='/image'>Image</a><br><br>" + \
                      "<p><u>Form Submission via GET</u></p>" + \
                      "<form action='/submit' method='GET'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>" + \
                      "<p><u>Form Submission via POST</u></p>" +\
                      "<form action='/submit' method='POST'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>"

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post_submit():
    conn = FakeConnection("POST /submit HTTP/1.1\r\n\r\n + \
                            firstname=Max&lastname=Sweet")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Mr. Max Sweet."

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
>>>>>>> master
