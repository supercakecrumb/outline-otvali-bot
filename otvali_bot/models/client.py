from sqlalchemy import Integer
from models import session, metadata, engine
from .models import Client
from typing import List



def get_client(username_or_id: str) -> Client:
    client = get_client_by_username(username_or_id)
    if client is None:
        client = get_client_by_id(username_or_id)
    if client is None:
        client = get_client_by_tg_id(username_or_id)
    return client


def get_clients() -> List[Client]:
    return session.query(Client).all()


def get_client_by_id(client_id: Integer) -> Client:
    return session.query(Client).filter(Client.id == client_id).first()


def get_client_by_username(username: str) -> Client:
    return session.query(Client).filter(Client.username == username).first()


def get_client_by_tg_id(client_tg_id: Integer) -> Client:
    return session.query(Client).filter(Client.tg_id == client_tg_id).first()


def save_new_client(tg_id: int, username: str):
    client = Client(tg_id, username)
    client.commit()


def approve_client(client: Client):
    client.is_approved = True
    client.is_declined = False
    client.commit()


def decline_client(client: Client):
    client.is_approved = False
    client.is_declined = True
    client.commit()


def give_client_admin_rights(client: Client):
    client.is_admin = True
    client.commit()


def get_wait_list():
    return session.query(Client).filter_by(is_approved=False, is_declined=False).all()


metadata.create_all(engine)
