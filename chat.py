#!/bin/env python
import logging

logging.basicConfig(level=logging.INFO)

from app import create_app, socketio

logging.getLogger('engineio').setLevel(logging.INFO)
logging.getLogger('socketio').setLevel(logging.INFO)


app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
