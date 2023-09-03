import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("BOT_TOKEN")
sql_engine_url = os.environ.get("SQL_ENGINE_URL", "sqlite:///app.db")
logging_config_path = os.environ.get("LOGGING_CONFIG_PATH", "logging.conf")
outline_service_url = os.environ.get("OUTLINE_SERVICE_URL", "http://0.0.0.0:5000")
webhook_host = os.environ.get("WEBHOOK_HOST")
webhook_port = os.environ.get("WEBHOOK_PORT", "80")
webhook_listen = os.environ.get("WEBHOOK_LISTEN", "0.0.0.0")
webhook_cert = os.environ.get("WEBHOOK_CERT")
webhook_priv = os.environ.get("WEBHOOK_PRIV")
webhook_url_path = os.environ.get("WEBHOOK_URL_PATH", "/api/web-hook/")
use_webhook = os.environ.get("USE_WEBHOOK", False)
admin_password = os.environ.get("ADMIN_PASSWORD", "roottoor")
