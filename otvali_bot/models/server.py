from models import session
from sqlalchemy.orm import joinedload
from .models import Server, Client

def get_all_servers(): 
    return session.query(Server).all()

def get_server_by_id(server_id: int):
    return session.query(Server).filter(Server.id == server_id).first()

def get_server_by_country(country: str):
    return session.query(Server).filter(Server.country == country).first()

def get_server_by_city(city: str):
    return session.query(Server).filter(Server.city == city).first()

def get_servers_by_client(client_id: int):
    client = session.query(Client).options(joinedload('servers')).filter(Client.id == client_id).first()
    if client:
        return client.servers
    else:
        return None
