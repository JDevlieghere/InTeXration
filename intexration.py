import configparser
import os
from intexration.server import Server


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
    if not 'server' in config:
        raise RuntimeError('No server information found in configuration file!')
    server = Server(host=config['server']['host'], port=config['server']['port'])
    server.start()

if __name__ == '__main__':
    main()