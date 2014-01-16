import configparser
import os
from intexration.server import Server


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-host', help='hostname', default='localhost')
    # parser.add_argument('-port', help='port', default=8000)
    # args = parser.parse_args()
    config = configparser.ConfigParser()
    if not os.path.isfile('config.ini'):
        raise RuntimeError('No configuration file found!')
    config.read('config.ini')
    if not 'server' in config:
        raise RuntimeError('No server information found in configuration file!')
    server = Server(host=config['server']['host'], port=config['server']['port'])
    server.start()

if __name__ == '__main__':
    main()