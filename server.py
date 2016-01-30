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

from game import *
from player import Player

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
game = Game([])
room = "hardcode me"

@app.route('/<username>', methods=['GET', 'POST'])
def login(username):
	if request.method == 'POST':
		return "post success woohooo!: " + username
	return "this is the login screen: " + username

@socketio.on('join')
def join(data):
    for player in game.players:
        if (data['name'] == player.get_name()):
            print 'Error, same name'
            emit('joinFailed', "Error: A player already has the same name!")
            return

    new_player = Player(data['name'], 'OBJOBJOBJ')
    game.players.append(new_player)
    print new_player.get_name() + ' has joined!'

    current_players_name = []
    for player in game.players:
        current_players_name.append(player.get_name())

    join_room(room)
    emit('joinSuccessful', current_players_name, room=room)

@socketio.on('move')
def doAction(data):
    from_player = data['from']
    player_action = data['action']
    options = None
    action = None

    for stuff in Action:
        if (stuff.name == player_action):
            action = stuff
            break;

    if (isinstance(action, Action)):
        game.handleAction(action, options)
    else:
        print 'Error, invalid action'

@socketio.on('leave')
def leave(data):
    player_name = data['name']
    game.playerLeft(player_name)
    print player_name + ' has left!'

    current_players_name = []
    for player in game.players:
        current_players_name.append(player.get_name())

    leave_room(room)
    emit('playerLeft', current_players_name, room=room)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
