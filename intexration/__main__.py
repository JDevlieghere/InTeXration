import argparse
import logging.config
import os
from intexration import settings
from intexration.server import Server

# Logger
logging.config.fileConfig(settings.LOGGING_FILE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='Change the hostname')
    parser.add_argument('-port', help='Change the port')

    args = parser.parse_args()
    if args.host is not None:
        settings.set_config('host', args.host)
        logging.INFO("Host changed to %s", args.host)
    if args.port is not None:
        settings.set_config('port', args.port)
        logging.INFO("Port changed to %s", args.port)

    if not settings.all_files_exist():
        raise RuntimeError("Some necessary files were missing. Please consult the log.")

    server = Server(host=settings.get_config('SERVER', 'host'),
                    port=settings.get_config('SERVER', 'port'))
    server.start()

if __name__ == '__main__':
    main()