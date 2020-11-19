import os
import functools
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def once(f):
    was = False
    res = None

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        nonlocal was, res
        if not was:
            res = f(*args, **kwargs)
            was = True
        return res

    return decorated

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']


@once
def create_db():
    engine = create_engine(f'postgres://{user}:{pwd}@db:5432/{db}')
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()
    return db_session, engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)

db_session, engine, Base = create_db()
