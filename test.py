import time
from celery import Celery

app = Celery('tasks',backend='rpc://', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    
    time.sleep(3)
    print("time sleep is done")
    return x + y 

@app.task
def printout(msg):
    time.sleep(5)
    print(msg)
    return msg
