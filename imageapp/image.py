# image handling API
import sqlite3
import sys

class Image:
    filename = ''
    data = ''
    score = 0
    content = ''
    name = ''	
    def __init__(self, filename, data, score, content, name):
        self.filename = filename
        self.data = data
        self.score = score
        self.content = content
        self.name = name

images = {}

def add_image(filename, data, content, name):
    # insert to database
    insert_image(filename, data, content, name)

def get_image(num):
    return retrieve_image(num)

def get_latest_image():
    return retrieve_image(-1)

def insert_image(filename, data, content, name):
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes

    # grab whatever it is you want to put in the database

    # insert!
    db.execute('INSERT INTO image_store (filename, score, image, content, name) \
        VALUES (?,?,?,?,?)', (filename, 1, data, content, name))
    db.commit()

# retrieve an image from the database.
def retrieve_image(i):
    # connect to database
    db = sqlite3.connect('images.sqlite')
    
    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    if i >= 0:
        c.execute('SELECT i, filename, score, image, content, name FROM image_store where i=(?)', (i,))
    else:
        c.execute('SELECT i, filename, score, image, content, name FROM image_store ORDER BY i DESC LIMIT 1')

    # grab the first result (this will fail if no results!)
    try:
        i, filename, score, image, content, name = c.fetchone()

        return Image(filename, image, score, content, name)
    except:
        pass

def add_comment(i, comment):
    db = sqlite3.connect('images.sqlite')
   
    if i == -1:
        c = db.cursor()

        # Latest image
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return

    db.execute('INSERT INTO image_comments (imageId, comment) VALUES (?,?)', (i, comment))
    db.commit()

def get_comments(i):
    comments = []
    db = sqlite3.connect('images.sqlite')

    # Get all the comments for this image
    c = db.cursor()
    if i == -1:
        # Latest image
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return

    c.execute('SELECT i, comment FROM image_comments WHERE imageId=(?) ORDER BY i DESC', (i,))
    for row in c:
        comments.append(row[1])

    return comments
	
def image_search(query):
    # connect to database
    db = sqlite3.connect('images.sqlite')

    # get a query handle (or "cursor")
    c = db.cursor()
	
    try:
        c.execute('SELECT i FROM image_store where name=(?)', (query,))
        val = int(c.fetchone()[0])
    except:
        c.execute('SELECT i FROM image_store where content=(?)', (query,))
        val = int(c.fetchone()[0])
    
	
   
    return val

def get_image_score(i):
    # connect to database
    db = sqlite3.connect('images.sqlite')

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    if i >= 0:
        c.execute('SELECT score FROM image_store where i=(?)', (i,))
    else:
        c.execute('SELECT score FROM image_store ORDER BY i DESC LIMIT 1')

    val = int(c.fetchone()[0])
    print val
    return val

def increment_image_score(i):
# connect to database
    db = sqlite3.connect('images.sqlite')

    if i < 0:
        i = get_num_images()

    db.execute('UPDATE image_store SET score = score + 1 where i=(?)', (i,))
    db.commit()

def decrement_image_score(i):
# connect to database
    db = sqlite3.connect('images.sqlite')

    if i < 0:
        i = get_num_images()

    db.execute('UPDATE image_store SET score = score - 1 where i=(?)', (i,))
    db.commit()

def get_num_images():
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
    try:
        return int(c.fetchone()[0])
    except:
        return 0