from sqlalchemy import create_engine, Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
Session = sessionmaker()

# Association table to manage many-to-many relationships between Client and Server
client_server_association = Table('client_server', Base.metadata,
                                  Column('client_id', Integer, ForeignKey('client.id')),
                                  Column('server_id', Integer, ForeignKey('server.id'))
                                  )

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer)
    username = Column(String)
    is_approved = Column(Boolean)
    is_declined = Column(Boolean)
    is_admin = Column(Boolean)

    # Many-to-Many relationship with Server
    servers = relationship("Server",
                           secondary=client_server_association,
                           back_populates="clients")

    def __init__(self, tg_id, username):
        self.tg_id = tg_id
        self.username = username
        self.is_approved = False
        self.is_declined = False
        self.is_admin = False

class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String)
    port = Column(Integer)
    country = Column(String)
    city = Column(String)
    num_users = Column(Integer)

    # Many-to-Many relationship with Client
    clients = relationship("Client",
                           secondary=client_server_association,
                           back_populates="servers")

engine = create_engine('sqlite:///outline_service.db')
Base.metadata.create_all(engine)
Session.configure(bind=engine)
