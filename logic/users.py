from flask_socketio import SocketIO


class Users:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio

    def login(self):
        pass

    def register(self):
        pass

    def user_exists(self):
        pass
