import logging
import os
import configparser

# Directories
ROOT = os.path.abspath(os.path.dirname(__file__))
CONFIG = os.path.join(ROOT, 'config')
DATA = os.path.join(ROOT, 'data')
TEMPLATES = os.path.join(ROOT, 'templates')

# Files
API_KEY_FILE = os.path.join(DATA, 'api_keys.csv')
CONFIG_FILE = os.path.join(CONFIG, 'settings.cfg')
LOGGING_FILE = os.path.join(CONFIG, 'logger.cfg')

# Configuration Keys
SERVER_KEY = 'SERVER'
HOST_KEY = 'host'
PORT_KEY = 'port'

# LateX Log
LOG_NEW_LINE_CHAR = '\n'
LOG_ERROR_STRING = '! '
LOG_WARNING_STRING = 'Warning'


def all_files_exist():
    if not os.path.exists(API_KEY_FILE):
        logging.error("File with API keys not found.")
        return False
    if not os.path.exists(CONFIG_FILE):
        logging.error("Configuration file not found.")
        return False
    if not os.path.exists(LOGGING_FILE):
        logging.error("Log configuration file not found.")
        return False
    return True


def get_config(section, key):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get(section, key)


def set_config(section, key, value):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        config.set(section, key, value)
    except configparser.ConfigParser.NoSectionError:
        config.add_section(section)
        set_config(section, key, value)

