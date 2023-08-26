from loggerconfig import getLogger
logger = getLogger(__name__)

from bot.bot import bot
import bot.answers as answers
from models.chat import sync_chat
from models.client import handle_client, handle_admin
logger.info("Starting bot ")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    handle_client(message)
    logger.info(f'{message.from_user.username} sent {message.text}')
    bot.send_message(message.chat.id, "Your request has been sent to the supervisor, wait for the approvement")

@bot.message_handler(commands=['assign_admin'])
def assign_admin(message):
    callback = bot.send_message(message.chat.id, "Please enter the password to receive admin rights")
    logger.info(f'{message.from_user.username} tried to receive admin rights')
    bot.register_next_step_handler(callback, receive_password)

@bot.message_handler(content_types=['text'])
def receive_password(message):
    if handle_admin(message):
        logger.info(f'{message.from_user.username} received admin rights')
        bot.send_message(message.chat.id, "Now you're admin!")
    else:
        bot.send_message(message.chat.id, "Wrong password! Fuck off")
    bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=['help'])
def send_help(message):
    sync_chat(message)
    logger.info(f'{message.from_user.username} sent {message.text}')
    bot.send_message(message.chat.id, answers._help)


@bot.message_handler(func=lambda m: True)
def error(message):
    sync_chat(message)
    logger.info(f'{message.from_user.username} sent {message.text}')
    bot.reply_to(message, answers.error)    
