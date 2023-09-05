from .mytelebot import myTeleBot
from models.client import *
from models.server import *
from models.utils import client_has_key
from time import sleep
from outline_service.outline_getter import OutlineGetter
from .utils import get_country_emoji, delete_message_after_a_minute, is_convertible_to_int
from telebot import types
import threading

MESSAGE_DELETION_TIMEOUT = 60
OUTLINE_SERVER_MENU_CALLBACK_PREFIX = "server_menu"

def handle_server_menu_callback(bot: myTeleBot, call: types.CallbackQuery):
    bot.logger.debug(f"Recieved server menu callback from {call.from_user.username}: {call.data}")
    server_id = call.data.replace(f"{OUTLINE_SERVER_MENU_CALLBACK_PREFIX}_", "")

    if not is_convertible_to_int(server_id):
        bot.logger.Error(f"Server menu button error: cannot parse to int {server_id}")
        bot.answer_callback_query(callback_query_id=call.id, text="Something went wrong", show_alert=False)
        bot.edit_message_text("Something went wrong, we already trying to fix it. Try later pls.", call.message.chat.id, call.message.message_id, reply_markup=None)
        return
    
    server_id = int(server_id)

    server = get_server_by_id(server_id)
    client = get_client(call.from_user.id)

    if server:
        outline_service = OutlineGetter.get_instance()

        if not client_has_key(client.id, server.id):
            outline_service.create_user(client.id, server.id)
            bot.edit_message_text("Creating a key...", call.message.chat.id, call.message.message_id, reply_markup=None)
            sleep(1)
        else:
            bot.edit_message_text("Sending a key...", call.message.chat.id, call.message.message_id, reply_markup=None)
            
        key_info = outline_service.get_key(client.id, server.id)
        
        if key_info:
            sent_message = bot.send_message(call.message.chat.id, f"```{key_info}```", parse_mode='Markdown')
            threading.Thread(target=delete_message_after_a_minute, args=(bot, call.message.chat.id, sent_message.message_id, MESSAGE_DELETION_TIMEOUT)).start()
            bot.edit_message_text(f"Your key for {get_country_emoji(server.country)} {server.city}, {server.country} has been sent. Message with key will be deleted in 1 minute.", call.message.chat.id, call.message.message_id, reply_markup=None)
            bot.logger.info(f"Key sent to {call.message.from_user.username}")
        else:
            bot.logger.error(f"Key from server {server.id} for user {client.username} wasn't found.")
            bot.answer_callback_query(callback_query_id=call.id, text="Something went wrong", show_alert=False)
            bot.edit_message_text("Something went wrong, we already trying to fix it. Try later pls.", call.message.chat.id, call.message.message_id, reply_markup=None)
            return
    else:
        bot.logger.Error(f"Server menu button error: cannot find server {server_id}")
        bot.answer_callback_query(callback_query_id=call.id, text="Something went wrong", show_alert=False)
        bot.edit_message_text("Something went wrong, we already trying to fix it. Try later pls.", call.message.chat.id, call.message.message_id, reply_markup=None)


    bot.answer_callback_query(callback_query_id=call.id, text="", show_alert=False)
    

def server_menu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    servers = get_all_servers()

    buttons = ([types.InlineKeyboardButton(f"{get_country_emoji(server.country)} {server.city}, {server.country}", callback_data=f"{OUTLINE_SERVER_MENU_CALLBACK_PREFIX}_{server.id}") for server in servers])
    for b in buttons:
        markup.add(b)

    return markup


def setup_outline_commands(bot: myTeleBot):

    @bot.message_handler(commands=['get_key'])
    def get_key(message: types.Message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        markup = server_menu_markup()
        bot.send_message(message.chat.id, "Choose a server:", reply_markup=markup)


    @bot.message_handler(commands=['server_list'])
    def server_list(message: types.Message):
        bot.logger.info(f"Received server_list command from chat ID: {message.chat.id}")
        servers = get_all_servers()

        if servers:
            servers_str = "\n".join([f"{get_country_emoji(server.country)} {server.id}. {server.city}, {server.country}" for server in servers])
            bot.send_message(message.chat.id, f"Available servers:\n{servers_str}")
        else:
            bot.send_message(message.chat.id, "No servers found.")
