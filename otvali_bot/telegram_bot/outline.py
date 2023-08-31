from .mytelebot import myTeleBot
from models.client import *
from outline_service.outline_getter import OutlineGetter

def setup_outline_commands(bot: myTeleBot):
    @bot.message_handler(commands=['get_key'])
    def get_key(message):
        try:
            key_id = int(message.text.split(' ')[1])
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Usage: /get_key <int:key_id>")
            return

        otline_service = OutlineGetter.get_instance()  # Fetch the singleton instance
        key_info = otline_service.get_key(key_id)  # Assuming your client has a method get_key()

        if key_info:
            bot.send_message(message.chat.id, f"Your key: {key_info}")
        else:
            bot.send_message(message.chat.id, "Key not found.")

    @bot.message_handler(commands=['my_keys'])
    def my_keys(message):
        otline_service = OutlineGetter.get_instance()
        keys = otline_service.get_keys()  # Assuming your client has a method get_keys()

        if keys:
            keys_str = "\n".join([f"{key['id']} - {key['info']}" for key in keys])
            bot.send_message(message.chat.id, f"Your keys:\n{keys_str}")
        else:
            bot.send_message(message.chat.id, "No keys found.")

    @bot.message_handler(commands=['server_list'])
    def server_list(message):
        otline_service = OutlineGetter.get_instance()
        servers = otline_service.get_servers()  # Assuming your client has a method get_servers()

        if servers:
            servers_str = "\n".join([f"{server['id']} - {server['name']}" for server in servers])
            bot.send_message(message.chat.id, f"Available servers:\n{servers_str}")
        else:
            bot.send_message(message.chat.id, "No servers found.")