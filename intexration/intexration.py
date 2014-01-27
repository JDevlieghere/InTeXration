import logging
import os
import configparser
import shutil
from intexration import constants
from intexration.manager import ApiManager
from intexration.singleton import Singleton


class IntexrationParser:

    def __init__(self, arguments, config):
        self.arguments = arguments
        self.config = config

    def get(self, argument):
        return getattr(self.arguments, argument)

    def is_set(self, argument):
        return hasattr(self.arguments, argument) and getattr(self.arguments, argument) is not None

    def is_true(self, argument):
        return hasattr(self.arguments, argument) and hasattr(self.arguments, argument)

    def parse(self):
        self.parse_config()
        self.parse_api()

    def parse_config(self):
        if self.is_set('config_host'):
            self.config.write('SERVER', 'host', self.get('config_host'))
        if self.is_set('config_port'):
            self.config.write('SERVER', 'port', self.get('config_port'))
        if self.is_set('config_export'):
            self.config.file_export(self.get('config_export'))
        if self.is_set('config_import'):
            self.config.file_import(self.get('config_import'))

    def parse_api(self):
        api_manager = ApiManager()
        if self.is_set('api_add'):
            api_manager.add_key(self.get('api_add'))
        if self.is_set('api_remove'):
            api_manager.remove_key(self.get('api_remove'))
        if self.is_true('api_list'):
            for line in api_manager.all_keys():
                print(line[0])
        if self.is_set('api_export'):
            api_manager.export_file(self.get('api_export'))
        if self.is_set('api_import'):
            api_manager.import_file(self.get('api_import'))


@Singleton
class IntexrationConfig:

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.settings_file = os.path.join(constants.DIRECTORY_ROOT, constants.DIRECTORY_CONFIG, constants.FILE_SETTINGS)
        self.logger_file = os.path.join(constants.DIRECTORY_ROOT, constants.DIRECTORY_CONFIG, constants.FILE_LOGGER)

    def validate(self):
        if not os.path.exists(self.settings_file):
            raise RuntimeError("Settings file missing")
        if not os.path.exists(self.logger_file):
            raise RuntimeError("Logger config file missing")
        try:
            self.read('SERVER', 'host')
            self.read('SERVER', 'port')
            self.read('COMPILATION', 'branch')
            self.read('COMPILATION', 'lazy')
            self.read('COMPILATION', 'threaded')
        except configparser.Error:
            raise RuntimeError("Invalid config file")

    def read(self, section, key):
        file = self.file_path('config')
        self.parser.read(file)
        return self.parser[section][key]

    def read_bool(self, section, key):
        return self.str2bool(self.read(section, key))

    def write(self, section, key, value):
        file = self.file_path('config')
        self.parser.read(file)
        self.parser.set(section, key, value)
        with open(file, 'w+') as configfile:
            self.parser.write(configfile)
        logging.info("Updated config %s = %s", [key, value])

    def file_export(self, directory):
        path = os.path.join(directory, self.file_name('config'))
        shutil.copyfile(self.file_path('config'), path)
        logging.info("Configuration exported to %s", path)

    def file_import(self, directory):
        path = os.path.join(directory, self.file_name('config'))
        if not os.path.exists(path):
            raise RuntimeError("Importing configuration failed: not found in %s", path)
        shutil.copyfile(path, self.file_path('config'))
        self.validate()
        logging.info("Configuration imported from %s", path)

    def base_url(self):
        return 'http://'+self.read('SERVER', 'host')+':'+self.read('SERVER', 'port')+'/'

    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")