from models import session
from sqlalchemy.orm import joinedload
from .models import Server, Client

def client_has_key(client_id: int, server_id: int):
    client = session.query(Client).options(joinedload(Client.servers)).filter_by(id=client_id).one_or_none()
    if not client:
        return False
    return any(server.id == server_id for server in client.servers)
