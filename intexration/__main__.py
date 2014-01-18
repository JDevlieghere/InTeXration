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
    parser.add_argument('-list', help='List API keys', action='store_true')

    if not settings.all_files_exist():
        raise RuntimeError("Some necessary files were missing. Please consult the log.")

    quit_when_done = False
    args = parser.parse_args()
    if args.host is not None:
        settings.set_config('SERVER', 'host', args.host)
        logging.info("Host changed to %s", args.host)
        quit_when_done = True
    if args.port is not None:
        settings.set_config('SERVER', 'port', args.port)
        quit_when_done = True
        logging.info("Port changed to %s", args.port)
    if args.add is not None:
        ApiHelper(settings.API_KEY_FILE).add(args.add)
        logging.info("API key added.")
        quit_when_done = True
    if args.remove is not None:
        ApiHelper(settings.API_KEY_FILE).remove(args.remove)
        logging.info("API key %s removed.", args.remove)
        quit_when_done = True
    if args.list is not None:
        for line in ApiHelper(settings.API_KEY_FILE).get_all():
            print(line[0])
        quit_when_done = True
    if quit_when_done:
        quit()

    server = Server(host=settings.get_config('SERVER', 'host'),
                    port=settings.get_config('SERVER', 'port'))
    server.start()

if __name__ == '__main__':
    main()