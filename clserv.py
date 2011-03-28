#!/usr/bin/env python

import sys, os, cgi, xml.dom.minidom, sqlite3

# uncomment to enable error output in browser
sys.stderr = sys.stdout

print 'Content-Type: text/plain'
print

# set up CGI (input data)
field = cgi.FieldStorage()

# set up SQL (store data)
conn = sqlite3.connect('clsql.db')
curs = conn.cursor()
curs.execute('create table if not exists main (ip, text)')

# set up XML (output data)
impl  = xml.dom.minidom.getDOMImplementation()
doc = impl.createDocument(None, 'cls', None)
top = doc.documentElement
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

# create log element
log = addElement('log', top, {})
def addLog(entry):
    '''Append a string to the log element.
    
    Keyword arguments:
    entry -- a string to be added to the log.
    
    '''
    entrynode = doc.createTextNode(entry)
    log.appendChild(entrynode)


# close SQL
conn.commit()
curs.close()

# print XML
print doc.toprettyxml(indent=' '*4,encoding='utf-8')
