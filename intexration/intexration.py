import logging
import os
import configparser
import shutil
from intexration.singleton import Singleton


@Singleton
class IntexrationConfig:

    file_names = {
        'config': 'settings.cfg',
        'api': 'api_keys.csv',
        'logger': 'logger.cfg'
    }

    dir_names = {
        'config': 'config',
        'data': 'data',
        'templates': 'templates',
        'static': 'static'
    }

    constants = {
        'separator': '/',
        'latex_error': ' !',
        'latex_warning': 'Warning'
    }

    def __init__(self):
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.config = configparser.ConfigParser()

    def dir_path(self, name):
        return os.path.join(self.root, self.dir_names[name])

    def file_path(self, name):
        return os.path.join(self.root, self.file_names[name])

    def constant(self, name):
        return self.constants[name]

    def validate(self):
        for file in self.file_names:
            if not os.path.exists(self.file_path(file)):
                raise RuntimeError("Config files missing")
        for dir in self.dir_names:
            if not os.path.exists(self.dir_path(dir)):
                raise RuntimeError("Config directories missing")
        try:
            self.read('SERVER', 'host')
            self.read('SERVER', 'port')
            self.read('COMPILATION', 'branch')
            self.read('COMPILATION', 'lazy')
        except configparser.Error:
            raise RuntimeError("Invalid config file")

    def read(self, section, key):
        file = self.file_path('config')
        self.config.read(file)
        return self[section][key]

    def write(self, section, key, value):
        file = self.file_path('config')
        self.config.read(file)
        self.config.set(section, key, value)
        with open(file, 'w+') as configfile:
            self.config.write(configfile)

    def file_export(self, dir):
        path = os.path.join(dir, self.file_names('config'))
        shutil.copyfile(self.file_path('cnfig'), path)
        logging.info("Configuration exported to %s", path)

    def file_import(self, dir):
        path = os.path.join(dir, self.file_names('config'))
        if not os.path.exists(path):
            raise RuntimeError("Importing configuration failed: not found in %s", path)
        shutil.copyfile(path, self.file_path('cnfig'))
        self.validate()
        logging.info("Configuration imported from %s", path)

    def server_root(self):
        return 'http://'+self.read('SERVER', 'host')+':'+self.read('SERVER', 'port')+'/'