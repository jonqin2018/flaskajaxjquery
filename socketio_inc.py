
from flask_socketio import SocketIO, Namespace, emit
from flask import Flask

app = Flask(__name__)
socketio = SocketIO(app, async_handlers=True, ping_timeout=1800)

