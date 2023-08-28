
from bot.utils import admin_only
from loggerconfig import getLogger

logger = getLogger(__name__)
from bot.bot import bot
from models.client import get_user, get_wait_list, approve_client, decline_client


@bot.message_handler(commands=['waiting_list'])
@admin_only
def waiting_list(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    clients = get_wait_list()
    clients_list = str()
    number = 1
    for client in clients:
        clients_list += f"{number}. id: {client.id}, username: @{client.username}, telegram_id: {client.tg_id}\n"
        number += 1
    if clients_list == "":
        clients_list = "There are no clients on the waiting list!"
    bot.send_message(message.chat.id, clients_list)


@bot.message_handler(commands=['approve'])
@admin_only
def client_approve(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    identity = message.text.split(' ')[1]
    client = get_user(identity)
    if client is None:
        bot.send_message(message.chat.id, "This user hasn't been found!")
        return
    if client.is_approved:
        bot.send_message(message.chat.id, "This user has already been approved!")
    else:
        approve_client(client)
        bot.send_message(message.chat.id, "This user was approved!")
        bot.send_message(client.tg_id, "You have been approved!")


@bot.message_handler(commands=['approve_all'])
@admin_only
def client_approve_all(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    clients = get_wait_list()
    for client in clients:
        client.is_approved = True
        approve_client(client)
        bot.send_message(client.tg_id, "You have been approved!")
    bot.send_message(message.chat.id, "All clients were approved!")


@bot.message_handler(commands=['decline'])
@admin_only
def client_decline(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    identity = message.text.split(' ')[1]
    client = get_user(identity)
    if client is None:
        bot.send_message(message.chat.id, "This user hasn't been found!")
        return
    if client.is_declined:
        bot.send_message(message.chat.id, "This user has already been declined!")
    else:
        decline_client(client)
        bot.send_message(message.chat.id, "This user was declined!")
        bot.send_message(client.tg_id, "You have been declined!")


@bot.message_handler(commands=['decline_all'])
@admin_only
def client_decline_all(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    clients = get_wait_list()
    for client in clients:
        decline_client(client)
        bot.send_message(client.tg_id, "You have been declined!")
    bot.send_message(message.chat.id, "All clients were declined!")

