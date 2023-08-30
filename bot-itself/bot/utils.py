import os
from loggerconfig import getLogger

from bot.bot import bot
from models.client import get_client_by_tg_id, give_client_admin_rights

logger = getLogger(__name__)


def admin_only(func):
    def wrapper(message):
        client = get_client_by_tg_id(message.from_user.id)
        if client is None or (not client.is_admin):
            bot.send_message(message.chat.id, "You do not have admin rights to do it!")
            return
        return func(message)

    return wrapper


def receive_password(message):
    if message.text == os.environ.get("PASSWORD"):
        client = get_client_by_tg_id(message.from_user.id)
        if client is not None:
            give_client_admin_rights(client)
            logger.info(f'{message.from_user.username} received admin rights')
            bot.send_message(message.chat.id, "Now you're admin!")
    else:
        bot.send_message(message.chat.id, "Wrong password! Fuck off")
    bot.delete_message(message.chat.id, message.message_id)
