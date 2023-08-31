import os
from dotenv import load_dotenv

load_dotenv()

sql_engine_url = os.environ.get("SQL_ENGINE_URL", "sqlite:///app.db")
logging_config_path = os.environ.get("LOGGING_CONFIG_PATH", "logging.conf")
outline_service_url = os.environ.get("OUTLINE_SERVICE_URL", "http://0.0.0.0:5000")
