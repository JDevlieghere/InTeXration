import configparser
import os
from intexration.server import Server

server_key = 'SERVER'
host_key = 'host'
port_key = 'port'

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-host', help='hostname', default='localhost')
    # parser.add_argument('-port', help='port', default=8000)
    # args = parser.parse_args()
    path = os.path.join('config', 'config.ini')
    config = configparser.ConfigParser()
    if not os.path.isfile(path):
        raise RuntimeError('No configuration file found!')
    config.read(path)
    if not server_key in config:
        raise RuntimeError('No server information found in configuration file!')
    server = Server(host=config[server_key][host_key], port=config[server_key][port_key])
    server.start()

if __name__ == '__main__':
    main()