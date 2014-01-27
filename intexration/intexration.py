import logging
import os
import configparser
import shutil
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
        api_manager = ApiManager(self.config.file_path('api'))
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

    file_names = {
        'config': 'config/settings.cfg',
        'api': 'data/api_keys.csv',
        'logger': 'config/logger.cfg'
    }

    dir_names = {
        'views': 'views',
        'static': 'static',
        'temp': 'temp',
        'output': 'out'
    }

    constants = {
        'separator': '/',
        'newline': '\n',
        'latex_error': ' !',
        'latex_warning': 'Warning'
    }

    def __init__(self):
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.config = configparser.ConfigParser()

    def dir_path(self, name):
        return os.path.join(self.root, self.dir_names[name])

    def dir_name(self, name):
        return self.dir_names[name]

    def file_path(self, name):
        return os.path.join(self.root, self.file_names[name])

    def file_name(self, name):
        return self.file_names[name].split(self.constants['separator'])[-1]

    def constant(self, name):
        return self.constants[name]

    def validate(self):
        for file in self.file_names:
            if not os.path.exists(self.file_path(file)):
                raise RuntimeError("Config files missing")
        for directory in self.dir_names:
            if not os.path.exists(self.dir_path(directory)):
                raise RuntimeError("Config directories missing")
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
        self.config.read(file)
        return self.config[section][key]

    def read_bool(self, section, key):
        return self.str2bool(self.read(section, key))

    def write(self, section, key, value):
        file = self.file_path('config')
        self.config.read(file)
        self.config.set(section, key, value)
        with open(file, 'w+') as configfile:
            self.config.write(configfile)
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