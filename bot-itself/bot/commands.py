from loggerconfig import getLogger
logger = getLogger(__name__)

from bot.bot import bot
import bot.answers as answers
from models.chat import sync_chat
logger.info("Starting bot ")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    sync_chat(message)
    logger.info(f'{message.from_user.username} sent {message.text}')
    bot.send_message(message.chat.id, answers.start)


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
