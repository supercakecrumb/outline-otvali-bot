from .server import Server
from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from models import base, session, metadata, engine
from models.modelclass import Model
from sqlalchemy.orm import relationship
from client import Client

client_server_association = Table(
    'client_server',
    metadata,
    Column('client_id', Integer, ForeignKey('client.id'), primary_key=True),
    Column('server_id', Integer, ForeignKey('server.id'), primary_key=True),
    Column('outline_id', String),
    UniqueConstraint('client_id', 'server_id', name='uix_1')
)

metadata.create_all(engine)