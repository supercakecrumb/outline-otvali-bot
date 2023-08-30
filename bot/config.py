import os
from dotenv import load_dotenv
load_dotenv()


IMAGE_UPLOAD_FOLDER=os.environ.get("IMAGE_UPLOAD_FOLDER")

class Bot():
    def __init__(self, token):
        self.token = token

bot = Bot(os.environ.get("BOT_TOKEN"))

bot.use_webhook = os.environ.get("USE_WEBHOOK")
bot.webhook_host = os.environ.get("WEBHOOK_HOST")
bot.webhook_port = os.environ.get("WEBHOOK_PORT")
bot.webhook_listen = os.environ.get("WEBHOOK_LISTEN")
bot.webhook_cert = os.environ.get("WEBHOOK_SSL_CERT")
bot.webhook_priv = os.environ.get("WEBHOOK_SSL_PRIV")

bot.webhook_url_base = f'https://{bot.webhook_host}'
bot.webhook_url_path = f'/api/web-hook/'