from config import bot as botconfig
from .mytelebot import myTeleBot
from .admin import setup_admin_commands
from .commands import setup_default_commands
from flask import Flask
import flask
import time


def init_bot(bot: myTeleBot):
    bot.remove_webhook()
    time.sleep(0.1)
    bot.logger.info("Bot initialized.")


def init_webhook(bot: myTeleBot, app: Flask, webhook_host: str, webhook_url_path: str,
                 webhook_listen: str, webhook_port: str):
    WEBHOOK_URL_BASE = f'https://{webhook_host}{webhook_url_path}'
    bot.set_webhook(url=WEBHOOK_URL_BASE)
    bot.logger.info("Webhook initialized.")

    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        return ''

    @app.route(botconfig.webhook_url_path, methods=['POST'])
    def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = myTeleBot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            flask.abort(403)

    app.run(host=webhook_listen,
            port=webhook_port,
            debug=True)


def init_message_handlers(bot: myTeleBot):
    setup_admin_commands(bot)
    setup_default_commands(bot)
