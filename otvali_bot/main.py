from telegram_bot.mytelebot import myTeleBot
from telegram_bot.bot import init_bot, init_message_handlers, init_webhook
from logger.logger import getLogger
from flask import Flask
from config.bot import *


if __name__ == "__main__":
    logger = getLogger(logging_config_path)

    logger.debug("reading config")

    logger.debug(f"token = {token}")
    logger.debug(bool(use_webhook))
    bot = myTeleBot(token, logger)
    init_bot(bot)

    init_message_handlers(bot)

    if use_webhook == "True":
        app = Flask(__name__)
        init_webhook(bot, app, webhook_host, webhook_url_path, webhook_listen, int(webhook_port))
    else:
        bot.polling(none_stop=True)