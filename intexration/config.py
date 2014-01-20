import logging
import os
import configparser

# Directories
import shutil

PATH_ROOT = os.path.abspath(os.path.dirname(__file__))
PATH_CONFIG = os.path.join(PATH_ROOT, 'config')
PATH_DATA = os.path.join(PATH_ROOT, 'data')
PATH_TEMPLATES = os.path.join(PATH_ROOT, 'templates')
PATH_STATIC = os.path.join(PATH_ROOT, 'static')
PATH_OUTPUT = os.path.join(PATH_ROOT, 'out')
PATH_BUILD = os.path.join(PATH_ROOT, 'build')

# Base names
BASENAME_CFG = 'settings.cfg'
BASENAME_API = 'api_keys.csv'
BASENAME_LOG = 'logger.cfg'

# Files
FILE_API_KEY = os.path.join(PATH_DATA, BASENAME_API)
FILE_CONFIG = os.path.join(PATH_CONFIG, BASENAME_CFG)
FILE_LOGGING = os.path.join(PATH_CONFIG, BASENAME_LOG)

# Configuration Keys
KEY_SERVER = 'SERVER'
KEY_HOST = 'host'
KEY_PORT = 'port'

# LateX Log
LOG_NEW_LINE_CHAR = '\n'
LOG_ERROR_STRING = '! '
LOG_WARNING_STRING = 'Warning'


def all_files_exist():
    if not os.path.exists(FILE_API_KEY):
        logging.error("File with API keys not found.")
        return False
    if not os.path.exists(FILE_CONFIG):
        logging.error("Configuration file not found.")
        return False
    if not os.path.exists(FILE_LOGGING):
        logging.error("Log configuration file not found.")
        return False
    return True


def read(section, key):
    config = configparser.ConfigParser()
    config.read(FILE_CONFIG)
    return config[section][key]


def write(section, key, value):
    config = configparser.ConfigParser()
    config.read(FILE_CONFIG)
    config.set(section, key, value)
    with open(FILE_CONFIG, 'w+') as configfile:
        config.write(configfile)


def export_file(dir):
    path = os.path.join(dir, BASENAME_CFG)
    shutil.copyfile(FILE_CONFIG, path)
    logging.info("Configuration exported to %s", path)


def import_file(dir):
    path = os.path.join(dir, BASENAME_CFG)
    if not os.path.exists(path):
        logging.error("Importing configuration failed: %s not found.", BASENAME_CFG)
        return
    shutil.copyfile(path, FILE_CONFIG)
    logging.info("Configuration imported from %s", path)

# Server Root
SERVER_ROOT = 'http://'+read('SERVER', 'host')+':'+read('SERVER', 'port')+'/'
