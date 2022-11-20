from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
app.debug = True
app.host = 'localhost'


@socketio.on('join')
def on_join(data):
    join_room(data["room"])
    emit('chat', data["username"] + ' has entered the room.', to=data["room"])

@socketio.on('leave')
def on_leave(data):
    leave_room(data["room"])
    emit('chat', data["username"] + ' has left the room.', to=data["room"])

@socketio.on('message')
def send_message(data):
    emit('chat', f'{data["username"]} {data["message"]}', to=data["room"])

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)

