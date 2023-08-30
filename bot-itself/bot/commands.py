import os

from bot.utils import receive_password
from loggerconfig import getLogger

from bot.bot import bot
from models.chat import sync_chat
from models.client import save_new_client, get_client_by_tg_id, give_client_admin_rights

logger = getLogger(__name__)
logger.info("Starting bot ")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    if message.chat.type == 'private':
        client = get_client_by_tg_id(message.from_user.id)
        if client is None:
            save_new_client(message.from_user.id, message.from_user.username)
            bot.send_message(message.chat.id, "Your request has been sent to the admin, wait for the approvement")
        else:
            if client.is_declined:
                bot.send_message(message.chat.id, "Sorry, but your request was declined")
            else:
                if client.is_approved:
                    bot.send_message(message.chat.id,
                                     "Your request already has been approved. In order to get VPN credentials write "
                                     "/get_creds")
                else:
                    bot.send_message(message.chat.id,
                                     "You already requested VPN credentials. We will notify you as soon as answers "
                                     "approves your request")


@bot.message_handler(commands=['assign_admin'])
def assign_admin(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    callback = bot.send_message(message.chat.id, "Please enter the password to receive admin rights")
    bot.register_next_step_handler(callback, receive_password)


@bot.message_handler(commands=['help'])
def send_help(message):
    sync_chat(message)
    logger.info(f'{message.from_user.username} sent {message.text}')
    bot.send_message(message.chat.id, "idk sorry")


@bot.message_handler(func=lambda m: True)
def error(message):
    sync_chat(message)
    logger.info(f'{message.from_user.username} sent {message.text}')
    bot.reply_to(message, "Error!")
