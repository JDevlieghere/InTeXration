import os

# Directories
ROOT = os.path.abspath(os.path.dirname(__file__))
CONFIG = os.path.join(ROOT, 'config')
DATA = os.path.join(ROOT, 'data')
TEMPLATES = os.path.join(ROOT, 'templates')

# Files
API_KEY_FILE = 'api_keys.csv'
CONFIG_FILE = 'settings.cfg'
LOGGING_FILE = 'logger.cfg'

# Configuration Keys
SERVER_KEY = 'SERVER'
HOST_KEY = 'host'
PORT_KEY = 'port'

# LateX Log
LOG_NEW_LINE_CHAR = '\n'
LOG_ERROR_STRING = '! '
LOG_WARNING_STRING = 'Warning'