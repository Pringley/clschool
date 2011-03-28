#!/usr/bin/env python
# clschool 0.0.1 - Command-Line School, a space-shooter programming game
# Copyright (C) 2011 Ben Pringle
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; widhout even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: ben@pringley.com

"""Framework code to respond to XMLHttpRequests.

Important variables:
field -- the cgi.FieldStorage object containing POST data
ip -- the IP address from which the request originates
sql -- the SQLlite cursor
doc -- the xml.dom.Document object
top -- the xml.dom.Element called "cls" (root XML element)

"""

import sys, os, cgi, xml.dom.minidom, sqlite3

# print header
print 'Content-Type: text/plain'
print

# uncomment to enable error output in browser
sys.stderr = sys.stdout

# set up CGI (input data)
field = cgi.FieldStorage()
ip = os.getenv('HTTP_CLIENT_IP') or os.getenv('HTTP_X_FORWARDED_FOR') or os.getenv('REMOTE_ADDR') or 'UNKNOWN'

# set up SQL (store data)
sqlite_connection = sqlite3.connect('clsql.db')
sql = sqlite_connection.cursor()
nonalpha = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
def sanitize(input_string):
    '''Given a string, strip all non-alphanumeric characters.'''
    input_string.translate(None, nonalpha)
    return input_string

# set up XML (output data)
dom_implementation  = xml.dom.minidom.getDOMImplementation()
doc = dom_implementation.createDocument(None, 'cls', None)
top = doc.documentElement
def addElement(name, parent, attributes):
    """Create a DOM element.
    
    Keyword arguments:
    name -- string with the element's name
    parent -- the parent element object
    attributes -- dictionary containing attributes and values

    """
    element = doc.createElement(name)
    for key in attributes.keys():
        element.setAttribute(key, attributes[key])
    parent.appendChild(element)
    return element

def done():
    """Close the connection to SQLite and print the XML document."""
    # close SQL
    sqlite_connection.commit()
    sql.close()

    # print XML
    print doc.toprettyxml(indent=' '*4,encoding='utf-8')

if __name__ == '__main__':
    addLog('Test run of clserv successful.')
    done()
