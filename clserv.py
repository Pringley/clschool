#!/usr/bin/env python

import sys, os, cgi, xml.dom.minidom, sqlite3

# uncomment to enable debugging
sys.stderr = sys.stdout

print 'Content-Type: text/plain'
print

# set up CGI (input data)
field = cgi.FieldStorage()

# set up XML (output data)
impl  = xml.dom.minidom.getDOMImplementation()
doc = impl.createDocument(None, 'cls', None)
top = doc.documentElement

# set up SQL (store data)
conn = sqlite3.connect('clsql.db')
curs = conn.cursor()
curs.execute('create table if not exists main (ip, text)')

def addElement(name, parent, attributes):
    '''Create a DOM element.
    
    Keyword arguments:
    name -- string with the element's name
    parent -- the parent element object
    attributes -- dictionary containing attributes and values

    '''
    element = doc.createElement(name)
    for key in attributes.keys():
        element.setAttribute(key, attributes[key])
    parent.appendChild(element)
    return element

# handle get request
if 'getip' in field:
    # input from CGI field
    ip = field['getip'].value

    # set up XML tag
    user = addElement('user', top, {'ip':ip})
    
    # append text from SQL data
    curs.execute('select * from main where ip=?',(ip,))
    for row in curs:
        addElement('text', user, {'value':row[1]})

# handle set request
if 'settext' in field:
    # get remote IP from environment variables
    ip = os.getenv('HTTP_CLIENT_IP') or os.getenv('HTTP_X_FORWARDED_FOR') or os.getenv('REMOTE_ADDR') or 'UNKNOWN'

    # input from CGI field
    text = field['settext'].value

    # set up XML tag
    user = addElement('user', top, {'ip':ip})

    # add to SQL database
    curs.execute('insert into main values (?,?)', (ip, text))

    # print all text (including prior insertions)
    curs.execute('select * from main where ip=?',(ip,))
    for row in curs:
        addElement('text', user, {'value':row[1]})
    

# close SQL
conn.commit()
curs.close()

# print XML
print doc.toprettyxml(indent=' '*4,encoding='utf-8')


