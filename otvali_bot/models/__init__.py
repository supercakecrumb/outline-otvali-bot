from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine('sqlite:///app.db', echo=False, connect_args={'check_same_thread': False})
base = declarative_base(bind=engine)
metadata = base.metadata
session = scoped_session(sessionmaker(bind=engine))

