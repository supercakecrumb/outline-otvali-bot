import os
from .utils import admin_only
from .mytelebot import myTeleBot
from models.client import *
from config.bot import admin_password

def setup_admin_commands(bot: myTeleBot):
    @bot.message_handler(commands=['become_admin'])
    def assign_admin(message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        callback = bot.send_message(message.chat.id, "Please enter the password to receive admin rights")
        bot.register_next_step_handler(callback, receive_password)

    def receive_password(message):
        if message.text == admin_password:
            client = get_client_by_tg_id(message.from_user.id)
            if client is not None:
                give_client_admin_rights(client)
                bot.logger.info(f'{message.from_user.username} received admin rights')
                bot.send_message(message.chat.id, "Now you're admin!")
        else:
            bot.send_message(message.chat.id, "Wrong password! Fuck off")
        bot.delete_message(message.chat.id, message.message_id)

    @bot.message_handler(commands=['waitlist'])
    @admin_only
    def waitlist(message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
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
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        username_or_id = message.text.split(' ')[1]
        client = get_client(username_or_id)
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
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        clients = get_wait_list()
        for client in clients:
            client.is_approved = True
            approve_client(client)
            bot.send_message(client.tg_id, "You have been approved!")
        bot.send_message(message.chat.id, "All clients were approved!")


    @bot.message_handler(commands=['decline'])
    @admin_only
    def client_decline(message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        username_or_id = message.text.split(' ')[1]
        client = get_client(username_or_id)
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
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        clients = get_wait_list()
        for client in clients:
            decline_client(client)
            bot.send_message(client.tg_id, "You have been declined!")
        bot.send_message(message.chat.id, "All clients were declined!")


    @bot.message_handler(commands=['users'])
    @admin_only
    def get_users(message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        users = get_clients()
        out = "\n".join(map(repr, users))
        bot.send_message(message.chat.id, "Found users:\n" + out)

