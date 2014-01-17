import os

# Paths
ROOT = os.getcwd()
CONFIG = config_folder = os.path.join(ROOT, 'config')

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