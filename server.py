#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json
from random import sample

from game import *
from player import Player

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
game = None
room = "hardcode me"
player_names = []

@app.route('/<username>', methods=['GET', 'POST'])
def login(username):
	if request.method == 'POST':
		return "post success woohooo!: " + username
	return "this is the login screen: " + username

@socketio.on('join')
def join(data):
    name = data['name']
    global player_names

    if name in player_names:
        print 'Error, same name'
        emit('joinFailed', "Error: A player already has the same name!")
        return

    player_names.append(name)
    print name + ' has joined!'

    join_room(room)
    emit('joinSuccessful', player_names, room=room)
    if len(player_names) == 4:
        global game
        game = Game(player_names)
        all_players_details = game.getAllPlayersSummaries()
        print all_players_details
        emit('startGame', player_names, room=room)

@socketio.on('move')
def doAction(data):
    from_player = data['from']
    raw_player_action = data['action']
    action = None

    for stuff in Action:
        if (stuff.name == raw_player_action):
            action = stuff
            break;

    if (isinstance(action, Action)):
        game.handleAction(from_player, action, data)
    else:
        print 'Error, invalid action'

@socketio.on('leave')
def leave(data):
    name = data['name']
    if game is not None:
        game.playerLeft(name)
    
    print name + ' has left!'

    global player_names
    player_names.remove(name)

    leave_room(room)
    emit('playerLeft', player_names, room=room)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
