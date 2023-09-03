from .mytelebot import myTeleBot
from models.client import *
from models.server import *
from outline_service.outline_getter import OutlineGetter
from .utils import get_country_emoji, delete_message_after_a_minute, is_convertible_to_int
import threading  # import the threading module

MESSAGE_DELETION_TIMEOUT = 60

def setup_outline_commands(bot: myTeleBot):

    @bot.message_handler(commands=['create_key'])
    def create_key_command(message):
        try:
            bot.logger.debug("Starting create_key_command function")
            client = get_client(message.chat.id)
            client_id = client.id
            bot.logger.debug(f"Retrieved client ID: {client_id}")

            args = message.text.split(' ')[1:]
            if not args:
                bot.send_message(message.chat.id, "You must specify a server by its ID, city, or country.")
                return

            query_value = " ".join(args)
            server = None

            if is_convertible_to_int(query_value):
                server = get_server_by_id(int(query_value))
            if server is None:
                server = get_server_by_city(query_value)
            if server is None:
                server = get_server_by_country(query_value)

            if server is None:
                bot.send_message(message.chat.id, f"Invalid query. No server found for {query_value}")
                return

            bot.logger.info(f"Server found: {server}")
            outline_service = OutlineGetter.get_instance()
            outline_service.create_user(client_id, server.id)
            bot.send_message(message.chat.id, f"Key created successfully! You can get it with /my_keys or /get_key <server>")
            
        except Exception as e:
            bot.logger.error(f"An error occurred in create_key_command: {e}")


    @bot.message_handler(commands=['get_key'])
    def get_key(message):
        bot.logger.info(f"Received get_key command from chat ID: {message.chat.id}")
        client = get_client(message.chat.id)
        client_id = client.id
        
        args = message.text.split(' ')[1:]
        if not args:
            bot.send_message(message.chat.id, f"You must specify a server by its ID, city, or country. Server {args} not found")
            bot.logger.error("Server information not provided.")
            return

        query_value = " ".join(args)
        server = None

        if is_convertible_to_int(query_value):
            server = get_server_by_id(int(query_value))
        if server is None:
            server = get_server_by_city(query_value)
        if server is None:
            server = get_server_by_country(query_value)
        if server is None:
            bot.send_message(message.chat.id, f"Invalid query type. Please specify 'id', 'city', or 'country'. Server {args} not found")
            bot.logger.error(f"Invalid query type. Server {args} not found.")
            return

        if server:
            otline_service = OutlineGetter.get_instance()
            key_info = otline_service.get_key(client_id, server.id)
            
            if key_info:
                sent_message = bot.send_message(message.chat.id, f"This message will be deleted in 1 minute\n\nYour key from server {get_country_emoji(server.country)} {server.city}, {server.country}:\n```{key_info}```", parse_mode='Markdown')
                threading.Thread(target=delete_message_after_a_minute, args=(bot, message.chat.id, sent_message.message_id, MESSAGE_DELETION_TIMEOUT)).start()
                bot.logger.info(f"Key sent to chat ID: {message.chat.id}")
            else:
                bot.send_message(message.chat.id, "Key not found.")
                bot.logger.error("Key not found.")
        else:
            bot.send_message(message.chat.id, "No servers found for your query.")
            bot.logger.error("No servers found for the query.")


    @bot.message_handler(commands=['my_keys'])
    def my_keys(message):
        bot.logger.info(f"Received my_keys command from chat ID: {message.chat.id}")
        client = get_client(message.chat.id)
        if client:
            accessible_servers = client.servers  
            
            if accessible_servers:
                servers_str = "\n".join([
                    f"{get_country_emoji(server.country)} {server.id}. {server.city}, {server.country}"
                    for server in accessible_servers
                ])
                bot.send_message(
                    message.chat.id,
                    f"This message will be deleted in 1 minute\n\nYou have keys in:\n{servers_str}\nWrite /get_key <server> to get one.",
                    parse_mode='Markdown'
                )
            else:
                bot.send_message(message.chat.id, "You have no accessible servers.")
        else:
            bot.send_message(message.chat.id, "Client not found.")


    @bot.message_handler(commands=['server_list'])
    def server_list(message):
        bot.logger.info(f"Received server_list command from chat ID: {message.chat.id}")
        servers = get_all_servers()

        if servers:
            servers_str = "\n".join([f"{get_country_emoji(server.country)} {server.id}. {server.city}, {server.country}" for server in servers])
            bot.send_message(message.chat.id, f"Available servers:\n{servers_str}")
        else:
            bot.send_message(message.chat.id, "No servers found.")
