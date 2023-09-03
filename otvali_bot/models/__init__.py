from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config.bot import sql_engine_url

engine = create_engine(sql_engine_url, echo=False)
base = declarative_base(bind=engine)
metadata = base.metadata
session = scoped_session(sessionmaker(bind=engine))

