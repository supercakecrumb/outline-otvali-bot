from .mytelebot import myTeleBot
from models.client import *
from models.server import *
from outline_service.outline_getter import OutlineGetter
from .utils import get_country_emoji, delete_message_after_a_minute
import threading  # import the threading module

MESSAGE_DELETION_TIMEOUT = 60

def setup_outline_commands(bot: myTeleBot):
    @bot.message_handler(commands=['get_key'])
    def get_key(message):
        client_id = get_client(message.chat.id)
        
        args = message.text.split(' ')[1:]
        if not args:
            bot.send_message(message.chat.id, "You must specify a server by its ID, city, or country.")
            return

        query_type = args[0].lower()
        query_value = " ".join(args[1:])
        if query_type == "id":
            server = get_server_by_id(int(query_value))
        elif query_type == "city":
            server = get_server_by_city(query_value)
        elif query_type == "country":
            server = get_server_by_country(query_value)
        else:
            bot.send_message(message.chat.id, "Invalid query type. Please specify 'id', 'city', or 'country'.")
            return

        if server:
            otline_service = OutlineGetter.get_instance()  # Fetch the singleton instance
            key_info = otline_service.get_key(client_id)  # Passing the client ID
            
            if key_info:
                sent_message = bot.send_message(message.chat.id, f"This message will be deleted in 1 minute\n```\nYour key: {key_info}\n```", parse_mode='Markdown')
                threading.Thread(target=delete_message_after_a_minute, args=(bot, message.chat.id, sent_message.message_id, MESSAGE_DELETION_TIMEOUT)).start()
            else:
                bot.send_message(message.chat.id, "Key not found.")
        else:
            bot.send_message(message.chat.id, "No servers found for your query.")

    @bot.message_handler(commands=['my_keys'])
    def my_keys(message):
        client = get_client(message.chat.id)
        if client:
            accessible_servers = client.servers  
            
            if accessible_servers:
                servers_str = "\n".join([
                    f"{get_country_emoji(server.country)} {server.id}. {server.city}, {server.country}"
                    for server in accessible_servers
                ])
                sent_message = bot.send_message(
                    message.chat.id,
                    f"This message will be deleted in 1 minute\n```\nYour keys:\n{servers_str}\n```",
                    parse_mode='Markdown'
                )
                threading.Thread(
                    target=delete_message_after_a_minute,
                    args=(bot, message.chat.id, sent_message.message_id, MESSAGE_DELETION_TIMEOUT)
                ).start()
            else:
                bot.send_message(message.chat.id, "You have no accessible servers.")
        else:
            bot.send_message(message.chat.id, "Client not found.")


    @bot.message_handler(commands=['server_list'])
    def server_list(message):
        servers = get_all_servers()

        if servers:
            servers_str = "\n".join([f"{get_country_emoji(server.country)} {server.id}. {server.city}, {server.country}" for server in servers])
            bot.send_message(message.chat.id, f"Available servers:\n{servers_str}")
        else:
            bot.send_message(message.chat.id, "No servers found.")
