from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Association table to model many-to-many relationships between Clients and Servers
client_server_association = Table('client_server', Base.metadata,
    Column('client_id', Integer, ForeignKey('client.id')),
    Column('server_id', Integer, ForeignKey('server.id')),
    Column('outline_id', String)
)

class Client(Base):
    __tablename__ = 'client'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer)
    username = Column(String)
    is_approved = Column(Boolean)
    is_declined = Column(Boolean)
    is_admin = Column(Boolean)

    # many-to-many relationship between clients and servers
    servers = relationship('Server', secondary=client_server_association, back_populates='clients')

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
    api_url = Column(String)
    cert_sha256 = Column(String)  # Assuming this is encrypted before storing

    # many-to-many relationship between servers and clients
    clients = relationship('Client', secondary=client_server_association, back_populates='servers')

def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session