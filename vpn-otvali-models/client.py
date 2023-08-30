from sqlalchemy import Boolean, Column, Integer, String
from models import base, session, metadata, engine
from models.modelclass import Model
from models.loggerconfig import getLogger

logger = getLogger(__name__)
logger.debug("Client importing.")


class Client(base, Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer)
    username = Column(String)
    is_approved = Column(Boolean)
    is_declined = Column(Boolean)
    is_admin = Column(Boolean)

    def __init__(self, tg_id: int, username: str):
        self.tg_id = tg_id
        self.username = username
        self.is_approved = False
        self.is_declined = False
        self.is_admin = False

        logger.debug("Initializated {}".format(self.__repr__()))

    def __repr__(self):
        return f'<tg_id={self.tg_id} \
        id={self.id} \
        username={self.username} \
        is_approved={self.is_approved} \
        is_declined={self.is_declined} \
        is_admin={self.is_admin}'


def get_client_by_tg_id(client_tg_id: Integer):
    return session.query(Client).filter(Client.tg_id == client_tg_id).first()


def get_user(username_or_id: str):
    client = get_client_by_username(username_or_id)
    if client is None:
        client = get_client_by_id(username_or_id)
    return client


def get_client_by_id(client_id: Integer):
    return session.query(Client).filter(Client.id == client_id).first()


def get_client_by_username(username: str):
    return session.query(Client).filter(Client.username == username).first()


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
