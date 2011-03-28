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

"""Used to register or join a game session."""

import clserv, os, re

# make sure the session name is specified
if not 'name' in clserv.field:
    clserv.addLog('Failed to specify name of session.')

# otherwise, attempt to join given session
else:
    # use ip address as identifier
    id = clserv.ip
    
    name = clserv.field['name'].value
    clserv.sql.execute('create table if not exists sessions (name, id)')
    
    # purge ip from other sessions
    clserv.sql.execute('delete from sessions where id=?', (id,))

    # get all current members of the session
    clserv.sql.execute('select id from sessions where name=?', (name,))
    players = clserv.sql.fetchall()
    tag = clserv.addElement('session', clserv.top, {'name':name})
    
    # can't join a session that's already full (has two players)
    if len(players) >= 2:
        players.setAttribute('in','false')

    # add user's ip to the session
    else:
        clserv.sql.execute('insert into sessions values (?,?)', (name,clserv.ip))
        tag.setAttribute('in','true')
        players.append([id])

    # display current members of the session
    for player in players:
        clserv.addElement('player', tag, {'id':player[0]})
        

clserv.done()
