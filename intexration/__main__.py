import argparse
import logging.config
from intexration.intexration import IntexrationConfig, IntexrationParser

# Config
from intexration.server import Server

config = IntexrationConfig.instance()

# Logger
logging.config.fileConfig(config.file_path('logger'))


def main():
    parser = argparse.ArgumentParser(prog='intexration')
    subparsers = parser.add_subparsers(help='subparser')

    config_parser = subparsers.add_parser('config', help='configuration')
    config_parser.add_argument('--host', help='change the hostname', dest='config_host')
    config_parser.add_argument('--port', help='change the port', dest='config_port')
    config_parser.add_argument('--export', metavar='DIR', help='export configuration file to given directory',
                               dest='config_export')
    config_parser.add_argument('--import', metavar='DIR', help='import configuration file from given directory',
                               dest='config_import')

    api_parser = subparsers.add_parser('api', help='API management')
    api_parser.add_argument('--add', metavar='KEY', help='add API key', dest='api_add')
    api_parser.add_argument('--remove', metavar='KEY', help='remove API key', dest='api_remove')
    api_parser.add_argument('--list', help='list API keys', action='store_true', dest='api_list')
    api_parser.add_argument('--export', metavar='DIR', help='export API key file to given directory', dest='api_export')
    api_parser.add_argument('--import', metavar='DIR', help='import API key file from given directory',
                            dest='api_import')

    arguments = parser.parse_args()
    IntexrationParser(arguments, config).parse()

    server = Server(host=config.read('SERVER', 'host'),
                    port=config.read('SERVER', 'port'),
                    branch=config.read('COMPILATION', 'branch'),
                    lazy=config.str2bool(config.read('COMPILATION', 'lazy')),
                    threaded=config.str2bool(config.read('COMPILATION', 'threaded')))
    server.start()

if __name__ == '__main__':
    main()
