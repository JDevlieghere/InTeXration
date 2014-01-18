import configparser
import logging.config
import os
from intexration import settings
from intexration.server import Server




# Logger
logging.config.fileConfig(os.path.join(settings.CONFIG, settings.LOGGING_FILE))


def main():
    config_path = os.path.join(settings.CONFIG, settings.CONFIG_FILE)
    api_keys_path = os.path.join(settings.CONFIG, settings.API_KEY_FILE)
    config = configparser.ConfigParser()
    if not os.path.isfile(config_path):
        raise RuntimeError('No configuration file found!')
    if not os.path.isfile(api_keys_path):
        open(api_keys_path, 'w+').close()
        logging.warning("No API key file found. Empty file %s created in the configuration directory.",
                        settings.API_KEY_FILE)
    config.read(config_path)
    if not settings.SERVER_KEY in config:
        raise RuntimeError('No server information found in configuration file!')
    server = Server(host=config[settings.SERVER_KEY][settings.HOST_KEY],
                    port=config[settings.SERVER_KEY][settings.PORT_KEY], api_keys=api_keys_path)
    server.start()

if __name__ == '__main__':
    print(settings.ROOT)
    main()