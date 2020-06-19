import time
from celery import Celery
app1 = Celery('tasks',backend='rpc://', broker='pyamqp://guest@localhost//')
# from flask_socketio import SocketIO, Namespace, emit


# socketio = SocketIO(message_queue='redis://localhost:6379/')
@app1.task
def add(x, y):
    
    time.sleep(3)
    print("time sleep is done")
    socketio.emit("test","hello this is Socketio talking...")
    print("after emit...")
    return x + y 

@app1.task
def printout(msg):
    time.sleep(5)
    print(msg)
    return msg

@app1.task
def message_add(result_add):
    while not result_add.ready():
        time.sleep(.5)
    if result_add.ready():
        print("finally true")
        socketio.emit("test", "add is done")