import logging, logging.config
from otvali_models.base import configure as configure_models
from otvali_models.chat import Chat  # Moved to after configure_models

logging.config.fileConfig("bot/logging.conf")
logger = logging.getLogger("otvali_bot")

configure_models(logger, "sqlite:///app.db")

chat = Chat(1, 1, "1", "1", "1")
chat.commit()
