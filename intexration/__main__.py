import argparse
import logging.config
import os
from intexration import config
from intexration.helper import ApiHelper
from intexration.server import Server

# Logger
logging.config.fileConfig(config.FILE_LOGGING)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='Change the hostname')
    parser.add_argument('-port', help='Change the port')
    parser.add_argument('-aa', help='Add API key')
    parser.add_argument('-ar', help='Remove API key')
    parser.add_argument('-al', help='List API keys', action='store_true')
    parser.add_argument('-ae', help='Export API key file to given directory')
    parser.add_argument('-ai', help='Improt API key file from given directory')
    parser.add_argument('-ce', help='Export configuration file to given directory')
    parser.add_argument('-ci', help='Import configuration file from given directory')

    if not config.all_files_exist():
        raise RuntimeError("Some necessary files were missing. Please consult the log.")

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
        ApiHelper(config.FILE_API_KEY).add(args.aa)
        logging.info("API key added.")
        config_mode = True
    if args.ar is not None:
        ApiHelper(config.FILE_API_KEY).remove(args.ar)
        logging.info("API key %s removed.", args.remove)
        config_mode = True
    if args.al:
        for line in ApiHelper(config.FILE_API_KEY).get_all():
            print(line[0])
        config_mode = True
    if args.ae:
        ApiHelper(config.FILE_API_KEY).export_file(args.ae)
        config_mode = True
    if args.ai:
        ApiHelper(config.FILE_API_KEY).export_file(args.ai)
        config_mode = True
    if args.ce:
        config.export_file(args.ce)
        config_mode = True
    if args.ci:
        config.import_file(args.cs)
        config_mode = True
    if config_mode:
        quit()

    server = Server(host=config.read('SERVER', 'host'),
                    port=config.read('SERVER', 'port'))
    server.start()

if __name__ == '__main__':
    main()
