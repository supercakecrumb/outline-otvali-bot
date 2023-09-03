import logging
import logging.config

def getLogger(logging_config_path) -> logging.Logger:
    logging.config.fileConfig(logging_config_path)
    return logging.getLogger("otvali_bot")