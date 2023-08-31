from .mytelebot import myTeleBot
from models.client import *
from models.server import *
from outline_service.outline_getter import OutlineGetter
from .utils import get_country_emoji, delete_message_after_a_minute, is_convertible_to_int
import threading  # import the threading module

MESSAGE_DELETION_TIMEOUT = 60

def setup_outline_commands(bot: myTeleBot):
    @bot.message_handler(commands=['get_key'])
    def get_key(message):
        client_id = get_client(message.chat.id)
        
        args = message.text.split(' ')[1:]
        if not args:
            bot.send_message(message.chat.id, f"You must specify a server by its ID, city, or country. Server {args} not found")
            return

        query_value = " ".join(args)
        server = None

        if is_convertible_to_int(query_value):
            server = get_server_by_id(int(query_value))
        if server == None:
            server = get_server_by_city(query_value)
        if server == None:
            server = get_server_by_country(query_value)
        if server == None:
            bot.send_message(message.chat.id, f"Invalid query type. Please specify 'id', 'city', or 'country'. Server {args} not found")
            return

        if server:
            otline_service = OutlineGetter.get_instance()
            key_info = otline_service.get_key(client_id)
            
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
