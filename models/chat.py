from loggerconfig import getLogger
from sqlalchemy import Boolean, Column, Integer, String
from models import base, metadata, engine
from models.modelclass import Model

logger = getLogger(__name__)
logger.debug("Chat importing.")


class Chat(base, Model):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    is_person = Column(Boolean, nullable=False)
    chat_title = Column(String)
    tg_id = Column(Integer, unique=True)
    tg_username = Column(String)

    def __init__(self, chat_id: int, is_person: bool, chat_title: str, tg_id: str, tg_username: str):
        self.chat_id = chat_id
        self.is_person = is_person

        self.chat_title = chat_title

        self.tg_username = tg_username
        self.tg_id = tg_id

        logger.debug("Initializated {}".format(self.__repr__()))

    def __repr__(self):
        return f'<Chat id={self.chat_id} \
is_person={self.is_person} \
chat_title={self.chat_title} \
tg_id={self.tg_id} \
tg_username={self.tg_username}'

metadata.create_all(engine)
