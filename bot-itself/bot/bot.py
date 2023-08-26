from loggerconfig import getLogger
logger = getLogger(__name__)
logger.info("Starting bot")

import time
from bot.mytelebot import myTeleBot
import telebot.types
import flask
from config import bot as botconfig

WEBHOOK_HOST = botconfig.webhook_host
WEBHOOK_PORT = botconfig.webhook_port  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = botconfig.webhook_listen  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = botconfig.webhook_cert  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = botconfig.webhook_priv  # Path to the ssl private key

WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}'
WEBHOOK_URL_PATH = f'/api/web-hook/'

bot = myTeleBot(botconfig.token)
bot.remove_webhook()
time.sleep(0.1)
logger.debug('remove_webhook')
app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

logger.debug("Bot inited.")

import bot.commands as commands

if int(botconfig.use_webhook):
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            debug=True)
    logger.info("Bot webhook works")
else:
    bot.polling(none_stop=True)

logger.info("Bot started")