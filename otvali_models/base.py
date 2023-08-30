from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from logging import Logger
from sqlalchemy.ext.declarative import declarative_base

engine = None
session = None
logger = None

Base = declarative_base()
metadata = Base.metadata

def configure(logger_instance: Logger, db_url: str):
    global engine, session, metadata, logger

    logger = logger_instance
    logger.debug("Creating engine...")
    engine = create_engine(db_url, echo=False, connect_args={'check_same_thread': False})

    metadata.bind = engine

    logger.debug("Creating session")
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    metadata.create_all(engine)
