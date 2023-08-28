from sqlalchemy import Boolean, Column, Integer, String, select
from models import base, session, metadata, engine
from models.modelclass import Model
import telebot
from telebot import types
from bot.bot import bot
import os
from loggerconfig import getLogger

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
        is_approved={self.is_approved} \
        is_declined={self.is_declined} \
        is_admin={self.is_admin}'


def get_client_by_tg_id(client_tg_id: Integer):
    return session.query(Client).filter(Client.tg_id == client_tg_id).first()
def get_client_by_id(client_id: Integer):
    return session.query(Client).filter(Client.id == client_id).first()
def get_client_by_username(username: str):
    return session.query(Client).filter(Client.username == username).first()
def save(tg_id: int, username: str):
    client = Client(tg_id, username)
    client.commit()

def save(client: Client):
    client.commit()

def get_wait_list():
    return session.query(Client).filter_by(is_approved=False, is_declined=False).all()

metadata.create_all(engine)
