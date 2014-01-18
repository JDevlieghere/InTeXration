import os

# Directories
ROOT = os.path.abspath(os.path.dirname(__file__))
CONFIG = config_folder = os.path.join(ROOT, 'config')
TEMPLATES = config_folder = os.path.join(ROOT, 'templates')

# Files
API_KEY_FILE = 'api_keys.txt'
CONFIG_FILE = 'config.ini'
LOGGING_FILE = 'logger.ini'

# Configuration Keys
SERVER_KEY = 'SERVER'
HOST_KEY = 'host'
PORT_KEY = 'port'

# LateX Log
LOG_NEW_LINE_CHAR = '\n'
LOG_ERROR_STRING = '! '
LOG_WARNING_STRING = 'Warning'