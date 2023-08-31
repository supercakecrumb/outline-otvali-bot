from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from models import base, session, metadata, engine
from models.modelclass import Model
from sqlalchemy.orm import relationship
from .associations import client_server_association
from .client import Client

class Server(base, Model):
    __tablename__ = 'server'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)
    city = Column(String)
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

from sqlalchemy.orm import joinedload

# Function to get a server by its ID
def get_server_by_id(server_id: int):
    return session.query(Server).filter(Server.id == server_id).first()

# Function to get servers by their country
def get_servers_by_country(country: str):
    return session.query(Server).filter(Server.country == country).all()

# Function to get servers by their city
def get_servers_by_city(city: str):
    return session.query(Server).filter(Server.city == city).all()

# Function to get the list of servers that a user has access to
def get_servers_by_client(client_id: int):
    client = session.query(Client).options(joinedload('servers')).filter(Client.id == client_id).first()
    if client:
        return client.servers
    else:
        return None
