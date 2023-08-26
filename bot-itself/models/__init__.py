from loggerconfig import getLogger
logger = getLogger(__name__)
logger.info("Starting db...")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

logger.debug("Creating engine.")
engine = create_engine('sqlite:///app.db', echo=False, connect_args={'check_same_thread': False})
logger.debug("Creating declarative base")
base = declarative_base(bind=engine)
logger.debug("Creating metadata.")
metadata = base.metadata
logger.debug("Creating session.")
session = scoped_session(sessionmaker(bind=engine))
logger.debug("DB engine started.")

