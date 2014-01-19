import logging
import os
import configparser

# Directories
PATH_ROOT = os.path.abspath(os.path.dirname(__file__))
PATH_CONFIG = os.path.join(PATH_ROOT, 'config')
PATH_DATA = os.path.join(PATH_ROOT, 'data')
PATH_TEMPLATES = os.path.join(PATH_ROOT, 'templates')
PATH_STATIC = os.path.join(PATH_ROOT, 'static')
PATH_OUTPUT = os.path.join(PATH_ROOT, 'out')
PATH_BUILD = os.path.join(PATH_ROOT, 'build')

# Files
FILE_API_KEY = os.path.join(PATH_DATA, 'api_keys.csv')
FILE_CONFI = os.path.join(PATH_CONFIG, 'settings.cfg')
FILE_LOGGING = os.path.join(PATH_CONFIG, 'logger.cfg')

# Configuration Keys
SERVER_KEY = 'SERVER'
HOST_KEY = 'host'
PORT_KEY = 'port'

# LateX Log
LOG_NEW_LINE_CHAR = '\n'
LOG_ERROR_STRING = '! '
LOG_WARNING_STRING = 'Warning'

def all_files_exist():
    if not os.path.exists(FILE_API_KEY):
        logging.error("File with API keys not found.")
        return False
    if not os.path.exists(FILE_CONFI):
        logging.error("Configuration file not found.")
        return False
    if not os.path.exists(FILE_LOGGING):
        logging.error("Log configuration file not found.")
        return False
    return True


def read(section, key):
    config = configparser.ConfigParser()
    config.read(FILE_CONFI)
    return config[section][key]


def write(section, key, value):
    config = configparser.ConfigParser()
    config.read(FILE_CONFI)
    config.set(section, key, value)
    with open(FILE_CONFI, 'w+') as configfile:
        config.write(configfile)

# Server Root
SERVER_ROOT = 'http://'+read('SERVER', 'host')+':'+read('SERVER', 'port')+'/'
