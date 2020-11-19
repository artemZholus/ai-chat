from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
from uuid import uuid1 as uuid_gen
from .db_models import UserSession, Message
from .db import db_session


@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        was = (db_session.query(UserSession)
                .filter((UserSession.user_name == name))
                .count() != 0)
        if was:
            chat_id, uuid, = (db_session.query(UserSession)
                    .filter((UserSession.user_name == name))
                    .with_entities(UserSession.id, UserSession.uuid)
                    .first())
            uuid = str(uuid)
            # load messages
            messages = (db_session.query(Message)
                        .filter(Message.chat_id == chat_id)
                        .all())
            messages = [(m.sender, m.message) for m in messages]
            session['history'] = messages
        else:
            uuid = str(uuid_gen())
            sess = UserSession(uuid=uuid, user_name=name)
            db_session.add(sess)
            db_session.commit()
        session['name'] = name
        session['room'] = uuid
        return redirect(url_for('.chat'))
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
