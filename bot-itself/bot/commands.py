from loggerconfig import getLogger

logger = getLogger(__name__)
import os
from bot.bot import bot
import bot.answers as answers
from models.chat import sync_chat
from models.client import save, get_client_by_id, get_client_by_username, get_wait_list

logger.info("Starting bot ")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    if message.chat.type == 'private':
        client = get_client_by_id(message.from_user.id)
        if client is None:
            save(message.from_user.id, message.from_user.username)
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
def admin_only(func):
    def wrapper(message):
        client = get_client_by_id(message.from_user.id)
        if client is None or (not client.is_admin):
            bot.send_message(message.chat.id, "You do not have admin rights to do it!")
            return
        return func(message)
    return wrapper

@bot.message_handler(commands=['waiting_list'])
@admin_only
def waiting_list(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    clients = get_wait_list()
    clients_list = str()
    number = 1
    for client in clients:
        clients_list += f"{number}. username: @{client.username}, telegram_id: {client.tg_id}\n"
        number += 1
    if clients_list == "":
        clients_list = "There are no clients on the waiting list!"
    bot.send_message(message.chat.id, clients_list)

@bot.message_handler(commands=['approve'])
def client_approve(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    username = message.text.split(' ')[1]
    client = get_client_by_username(username)
    if client is None:
        bot.send_message(message.chat.id, "This user hasn't been found!")
        return
    if client.is_approved:
        bot.send_message(message.chat.id, "This user has already been approved!")
    else:
        client.is_approved = True
        client.is_declined = False
        save(client)
        bot.send_message(message.chat.id, "This user was approved!")
@bot.message_handler(commands=['approve_all'])
@admin_only
def client_approve_all(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    clients = get_wait_list()
    for client in clients:
        client.is_approved = True
        save(client)
    bot.send_message(message.chat.id, "All clients were approved!")

@bot.message_handler(commands=['assign_admin'])
def assign_admin(message):
    logger.info(f'{message.from_user.username} sent {message.text}')
    callback = bot.send_message(message.chat.id, "Please enter the password to receive admin rights")
    bot.register_next_step_handler(callback, receive_password)

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

@bot.message_handler(content_types=['text'])
def receive_password(message):
    if message.text == os.environ.get("PASSWORD"):
        client = get_client_by_id(message.from_user.id)
        if client is not None:
            client.is_admin = True
            save(client)
            logger.info(f'{message.from_user.username} received admin rights')
            bot.send_message(message.chat.id, "Now you're admin!")
    else:
        bot.send_message(message.chat.id, "Wrong password! Fuck off")
    bot.delete_message(message.chat.id, message.message_id)
