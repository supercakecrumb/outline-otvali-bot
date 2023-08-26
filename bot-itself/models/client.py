from sqlalchemy import Boolean, Column, Integer, String
from models import base, session, metadata, engine
from models.modelclass import Model
import telebot
import os
from loggerconfig import getLogger
logger = getLogger(__name__)
logger.debug("Client importing.")


class Client(base, Model):
    __tablename__ = 'client'

    tg_id = Column(Integer, primary_key = True)
    is_approved = Column(Boolean)
    is_declined = Column(Boolean)
    is_admin = Column(Boolean)

    def __init__(self, tg_id: int, is_approved: bool, is_declined: bool, is_admin: bool):
        self.tg_id = tg_id
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
    if (message.chat.type == 'private'):
        client = session.query(Client).filter(Client.tg_id == message.from_user.id).first()
        if (client == None):
            client = Client(
                message.from_user.id,
                False,
                False,
                False
            )
            client.commit()
def handle_admin(message: telebot.types.Message):
    if (message.text == os.environ.get("PASSWORD")):
        client = session.query(Client).filter(Client.tg_id == message.from_user.id).first()
        if (client != None):
            client.is_admin = True
            client.commit()
            return True


    
metadata.create_all(engine)