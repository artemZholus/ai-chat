from .db import Base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime


class UserSession(Base):
    __tablename__ = 'user_sessions'
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    user_name = Column(String(64))


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('user_sessions.id'))
    sender = Column(String(64))
    message = Column(String(512))
    date = Column(DateTime())

    def __repr__(self):
        return f'<Message(chat_id={self.chat_id}, sender={self.sender}, message={self.message})>'
