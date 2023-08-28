from bot.bot import bot
from models.client import get_client_by_tg_id
def admin_only(func):
    def wrapper(message):
        client = get_client_by_tg_id(message.from_user.id)
        if client is None or (not client.is_admin):
            bot.send_message(message.chat.id, "You do not have admin rights to do it!")
            return
        return func(message)
    return wrapper
