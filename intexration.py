import configparser
import logging.config
import os
from intexration.server import Server

# Configuration Folder
config_folder = os.path.join(os.getcwd(), 'config')

# Configuration Files
api_keys_file = 'api_keys.txt'
config_file = 'config.ini'
logging_file = 'logger.ini'

# Configuration Keys
server_key = 'SERVER'
host_key = 'host'
port_key = 'port'

# Logger
logging.config.fileConfig(os.path.join(config_folder, logging_file))

def main():
    config_path = os.path.join(config_folder, config_file)
    api_keys_path = os.path.join(config_folder, api_keys_file)
    config = configparser.ConfigParser()
    if not os.path.isfile(config_path):
        raise RuntimeError('No configuration file found!')
    if not os.path.isfile(api_keys_path):
        open(api_keys_path, 'w+').close()
        logging.warning("No API key file found. Empty file %s created in the configuration directory.", api_keys_file)
    config.read(config_path)
    if not server_key in config:
        raise RuntimeError('No server information found in configuration file!')
    logging.error("TEST")
    server = Server(host=config[server_key][host_key], port=config[server_key][port_key], api_keys=api_keys_path)
    server.start()

if __name__ == '__main__':
    main()