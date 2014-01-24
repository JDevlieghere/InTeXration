import argparse
import logging.config
from intexration.helper import ApiHelper
from intexration.intexration import IntexrationConfig
from intexration.server import Server

# Config
config = IntexrationConfig.Instance()

# Logger
#logging.config.fileConfig(config.file_path('logger'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='Change the hostname')
    parser.add_argument('-port', help='Change the port')
    parser.add_argument('-aa', metavar='KEY', help='Add API key')
    parser.add_argument('-ar', metavar='KEY', help='Remove API key')
    parser.add_argument('-al', help='List API keys', action='store_true')
    parser.add_argument('-ae', metavar='DIR', help='Export API key file to given directory')
    parser.add_argument('-ai', metavar='DIR', help='Improt API key file from given directory')
    parser.add_argument('-ce', metavar='DIR', help='Export configuration file to given directory')
    parser.add_argument('-ci', metavar='DIR', help='Import configuration file from given directory')

    config_mode = False
    args = parser.parse_args()
    if args.host is not None:
        config.write('SERVER', 'host', args.host)
        logging.info("Host changed to %s", args.host)
        config_mode = True
    if args.port is not None:
        config.write('SERVER', 'port', args.port)
        config_mode = True
        logging.info("Port changed to %s", args.port)
    if args.aa is not None:
        ApiHelper(config.file_path('api')).add(args.aa)
        logging.info("API key added.")
        config_mode = True
    if args.ar is not None:
        ApiHelper(config.file_path('api')).remove(args.ar)
        logging.info("API key %s removed.", args.remove)
        config_mode = True
    if args.al:
        for line in ApiHelper(config.file_path('api')).get_all():
            print(line[0])
        config_mode = True
    if args.ae:
        ApiHelper(config.file_path('api')).export_file(args.ae)
        config_mode = True
    if args.ai:
        ApiHelper(config.file_path('api')).export_file(args.ai)
        config_mode = True
    if args.ce:
        config.file_export(args.ce)
        config_mode = True
    if args.ci:
        config.file_import(args.cs)
        config_mode = True
    if config_mode:
        quit()

    server = Server(host=config.read('SERVER', 'host'),
                    port=config.read('SERVER', 'port'),
                    branch=config.read('COMPILATION', 'branch'),
                    lazy=config.str2bool(config.read('COMPILATION', 'lazy')))
    server.start()

if __name__ == '__main__':
    main()
