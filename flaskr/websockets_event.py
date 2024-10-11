from flask_socketio import SocketIO
from flask_socketio import emit

socketio = SocketIO()

def init_socketio(app):
    socketio.init_app(app)

    @socketio.on('message')
    def handle_message(data):
        print('Received message: ' + data)
        emit('response', {'message': 'Message received!'})

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')