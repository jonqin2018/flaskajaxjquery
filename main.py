from app import app, socketio
import logging
import traceback

from logging.handlers import RotatingFileHandler
if __name__=="__main__":
    
    socketio.run(app, debug=True, host='localhost', port=5001)
    # handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.ERROR)
    # logger.addHandler(handler)
    # from test import add, printout
