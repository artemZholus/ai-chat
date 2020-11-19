import requests
import json
from time import sleep
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .db_models import Message, UserSession
from .db import db_session
import logging

logger = logging.getLogger(__name__)


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    messages = session.get('history')
    name = session.get('name')
    if messages is not None:
        text = '\n'.join(f'{m[0]}: {m[1]}' for m in messages)
        logger.info(f'loaded messages! texts:\n' + text)
    else:
        text = f'< {name} has entered the room >'
    join_room(room)
    emit('status', {'msg': text }, room=room)


def process_message(message, name=None, from_user=True, chat_id=None):
    room = session.get('room')
    user_message = message['msg'].strip()
    if name is None:
        user_name = session.get('name')
    else:
        user_name = name
    if chat_id is None:
        chat_id = (db_session.query(UserSession.id)
                   .filter((UserSession.uuid == room)).first())
    mess = Message(chat_id=chat_id, sender=user_name, message=user_message,)
    db_session.add(mess)
    logger.info(f'got message: {mess}')
    content = {
        'msg': user_message,
        'sender': user_name,
        'from_user': int(from_user)
    }
    emit('message', content, room=room)
    db_session.commit()


@socketio.on('respond', namespace='/chat')
def respond(message):
    content = message["content"]
    logger.info(f'reposnding to {content}')
    room = session.get('room')
    chat_id = db_session.query(UserSession.id).filter((UserSession.uuid == room)).first()
    history = (db_session
               .query(Message.message)
               .filter((Message.chat_id == chat_id))
               .all())
    history = history[-10:]
    history = [h[0] for h in history]
    logger.info(history)
    wrapped = '- ' + '\n- '.join(history)
    wrapped += '\n-'
    logger.info(wrapped)
    succ = False
    retries = 0
    while retries < 2:
        try:
            resp = requests.post('http://ai:5496/generate/',
                                 json={'text': wrapped})
            succ = True
            break
        except:
            retries += 1
            logger.info('sleeping for 2 minutes...')
            sleep(120)
    if not succ or resp.status_code != 200:
        reply = 'Я упал('
    else:
        reply = json.loads(resp.text)['reply'][0]
        reply = reply[len(wrapped):]
        dot_pos = len(reply)
        hyp_pos = len(reply)
        n_pos = len(reply)
        if '\n' in reply:
            n_pos = reply.index('\n')
        if '-' in reply:
            hyp_pos = reply.index('-')
        #if '.' in reply:
        #    dot_pos = reply.index('.')
        pos = min(hyp_pos, dot_pos, n_pos)
        reply = reply[:pos]
    reply = {
        'msg': reply
    }
    process_message(reply, name='ai', from_user=False, chat_id=chat_id)


@socketio.on('text', namespace='/chat')
def text(message):
    process_message(message, from_user=True)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

