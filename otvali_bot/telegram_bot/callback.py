from .mytelebot import myTeleBot
from models.client import *
from models.server import *
from outline_service.outline_getter import OutlineGetter
from .outline import OUTLINE_SERVER_MENU_CALLBACK_PREFIX
from .outline import handle_server_menu_callback
from telebot import types

def setup_callback_queries(bot: myTeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call: types.CallbackQuery):
        bot.logger.info(f"Recieved call from {call.from_user.username}: {call.data}")
        if call.message:
            if call.data.startswith(OUTLINE_SERVER_MENU_CALLBACK_PREFIX):
                handle_server_menu_callback(bot, call)
