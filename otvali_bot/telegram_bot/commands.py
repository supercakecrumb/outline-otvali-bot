from .mytelebot import myTeleBot
from models.chat import sync_chat
from models.client import save_new_client, get_client_by_tg_id

help_text = '''
🛡️ *OtVali Help* 🛡️

1. `Approval`
   - Wait for admin approval to gain access to our servers. You will be notified once approved.

2. `/server_list` 
   - Browse through a list of available servers to find one that suits your needs.

3. `/create_key <server>` e.g. /create_key Frankfurt
   - Generate a new access key for the server specified. Use server ID, city, or country as the parameter.

4. `/get_key <server>` e.g. /get_key Germany
   - Retrieve your generated key for immediate use. The message containing the key will be deleted after 1 minute for security.

5. `/my_keys`
   - View a list of servers for which you have an access key.

📌 *Note*: In future updates, you will need admin approval to access individual servers.
'''


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
        bot.send_message(message.chat.id, help_text)


    @bot.message_handler(func=lambda m: True)
    def error(message):
        sync_chat(message)
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        bot.reply_to(message, "Error!")
