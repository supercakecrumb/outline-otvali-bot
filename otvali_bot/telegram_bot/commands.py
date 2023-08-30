from .mytelebot import myTeleBot
from models.chat import sync_chat
from models.client import save_new_client, get_client_by_tg_id

def setup_default_commands(bot: myTeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
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


    @bot.message_handler(commands=['help'])
    def send_help(message):
        sync_chat(message)
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        bot.send_message(message.chat.id, "idk sorry")


    @bot.message_handler(func=lambda m: True)
    def error(message):
        sync_chat(message)
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        bot.reply_to(message, "Error!")
