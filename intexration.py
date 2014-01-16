import configparser
import os
from intexration.server import Server

# Application Constants
api_keys_file = 'api_keys.txt'
config_folder = 'config'
config_file = 'config.ini'
server_key = 'SERVER'
host_key = 'host'
port_key = 'port'


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-host', help='hostname', default='localhost')
    # parser.add_argument('-port', help='port', default=8000)
    # args = parser.parse_args()
    config_path = os.path.join(config_folder, config_file)
    api_keys_path = os.path.join(config_folder, api_keys_file)
    config = configparser.ConfigParser()
    if not os.path.isfile(config_path):
        raise RuntimeError('No configuration file found!')
    if not os.path.isfile(api_keys_path):
        raise RuntimeError('No file with API keys found!')
    config.read(config_path)
    if not server_key in config:
        raise RuntimeError('No server information found in configuration file!')
    server = Server(host=config[server_key][host_key], port=config[server_key][port_key], api_keys=api_keys_path)
    server.start()

if __name__ == '__main__':
    main()