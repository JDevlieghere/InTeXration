import argparse
import logging.config
from intexration import settings
from intexration.helper import ApiHelper
from intexration.server import Server

# Logger
logging.config.fileConfig(settings.LOGGING_FILE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='Change the hostname')
    parser.add_argument('-port', help='Change the port')
    parser.add_argument('-add', help='Add API key')
    parser.add_argument('-remove', help='Remove API key')
    parser.add_argument('-list', help='List API keys')

    args = parser.parse_args()
    if args.host is not None:
        settings.set_config('SERVER', 'host', args.host)
        logging.info("Host changed to %s", args.host)
    if args.port is not None:
        settings.set_config('SERVER', 'port', args.port)
        logging.info("Port changed to %s", args.port)
    if args.add is not None:
        ApiHelper(settings.API_KEY_FILE).add(args.add)
        logging.info("API key added.")
    if args.remove is not None:
        ApiHelper(settings.API_KEY_FILE).add(args.remove)
        logging.info("API key %s removed.", args.remove)
    if args.list is not None:
        for line in ApiHelper(settings.API_KEY_FILE).get_all():
            print(line)

    if not settings.all_files_exist():
        raise RuntimeError("Some necessary files were missing. Please consult the log.")

    server = Server(host=settings.get_config('SERVER', 'host'),
                    port=settings.get_config('SERVER', 'port'))
    server.start()

if __name__ == '__main__':
    main()