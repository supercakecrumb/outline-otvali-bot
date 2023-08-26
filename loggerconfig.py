import logging 
import logging.config

def getLogger(name):
    logging.config.fileConfig('logging.conf')
    return logging.getLogger(name)