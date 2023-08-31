from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint, Boolean
from models import metadata, engine, base
from models.modelclass import Model
from sqlalchemy.orm import relationship

client_server_association = Table(
    'client_server',
    metadata,
    Column('client_id', Integer, ForeignKey('client.id'), primary_key=True),
    Column('server_id', Integer, ForeignKey('server.id'), primary_key=True),
    Column('outline_id', String),
    UniqueConstraint('client_id', 'server_id', name='uix_1')
)

class Client(base, Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer)
    username = Column(String)
    is_approved = Column(Boolean)
    is_declined = Column(Boolean)
    is_admin = Column(Boolean)

    servers = relationship('Server', secondary=client_server_association, back_populates='clients')
    

    def __init__(self, tg_id: int, username: str):
        self.tg_id = tg_id
        self.username = username
        self.is_approved = False
        self.is_declined = False
        self.is_admin = False


    def __repr__(self):
        return f'<tg_id={self.tg_id} \
        id={self.id} \
        username={self.username} \
        is_approved={self.is_approved} \
        is_declined={self.is_declined} \
        is_admin={self.is_admin}'


class Server(base, Model):
    __tablename__ = 'server'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, unique=True)
    city = Column(String, unique=True)
    num_users = Column(Integer)
    api_url = Column(String, unique=True)
    cert_sha256 = Column(String)

    # many-to-many relationship between servers and clients
    clients = relationship('Client', secondary=client_server_association, back_populates='servers')

    def __init__(self, country: str, city: str, api_url: str, cert_sha256: str):
        self.country = country
        self.city = city
        self.api_url = api_url
        self.cert_sha256 = cert_sha256
        self.num_users = 0  # Initialized with 0 users

    def __repr__(self):
        return f'<id={self.id} \
        country={self.country} \
        city={self.city} \
        num_users={self.num_users} \
        api_url={self.api_url} \
        cert_sha256={self.cert_sha256}>'

metadata.create_all(engine)