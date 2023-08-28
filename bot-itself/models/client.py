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

    tg_id = Column(Integer, primary_key=True)
    username = Column(String)
    is_approved = Column(Boolean)
    is_declined = Column(Boolean)
    is_admin = Column(Boolean)

    def __init__(self, tg_id: int, username: str, is_approved: bool, is_declined: bool, is_admin: bool):
        self.tg_id = tg_id
        self.username = username
        self.is_approved = is_approved
        self.is_declined = is_declined
        self.is_admin = is_admin

        logger.debug("Initializated {}".format(self.__repr__()))

    def __repr__(self):
        return f'<tg_id={self.tg_id} \
        is_approved={self.is_approved} \
        is_declined={self.is_declined} \
        is_admin={self.is_admin}'


def handle_client(message: telebot.types.Message):
    if message.chat.type == 'private':
        client = session.query(Client).filter(Client.tg_id == message.from_user.id).first()
        if client is None:
            client = Client(
                message.from_user.id,
                message.from_user.username,
                False,
                False,
                False
            )
            client.commit()
            bot.send_message(message.chat.id, "Your request has been sent to the supervisor, wait for the approvement")
        else:
            if client.is_declined:
                bot.send_message(message.chat.id,"Your request has been sent to the supervisor, wait for the "
                                                 "approvement")
            else:
                if client.is_approved:
                    bot.send_message(message.chat.id,
                                     "Your request already has been approved. In order to get VPN credentials write "
                                     "/get_creds")
                else:
                    bot.send_message(message.chat.id,
                                     "You already requested VPN credentials. We will notify you as soon as supervisor "
                                     "approves your request")


def handle_admin(message: telebot.types.Message):
    if message.text == os.environ.get("PASSWORD"):
        client = session.query(Client).filter(Client.tg_id == message.from_user.id).first()
        if client is not None:
            client.is_admin = True
            client.commit()
            logger.info(f'{message.from_user.username} received admin rights')
            bot.send_message(message.chat.id, "Now you're admin!")
    else:
        bot.send_message(message.chat.id, "Wrong password! Fuck off")


def admin_only(func):
    def wrapper(message):
        client = session.query(Client).filter(Client.tg_id == message.from_user.id).first()
        if client is None or (not client.is_admin):
            bot.send_message(message.chat.id, "You do not have admin rights to do it!")
            return
        return func(message)

    return wrapper
def approve(message: telebot.types.Message):
    username = message.text.split(' ')[1]
    client = session.query(Client).filter(Client.username == username).first()
    if client is None:
        bot.send_message(message.chat.id, "This user haven't been found!")
        return
    if client.is_approved:
        bot.send_message(message.chat.id, "This user has already been approved!")
    else:
        client.is_approved = True
        client.is_declined = False
        client.commit()
        bot.send_message(message.chat.id, "This user was approved!")

def approve_all(message: telebot.types.Message):
    clients = session.query(Client).filter_by(is_approved=False, is_declined=False).all()
    for client in clients:
        client.is_approved = True
        client.commit()
    bot.send_message(message.chat.id, "All clients were approved!")
def get_wait_list():
    return session.query(Client).filter_by(is_approved=False, is_declined=False).all()


metadata.create_all(engine)
