import configparser
import os
import sys
from intexration.manager import ApiManager

__author__ = 'Jonas'


class BuildParser:

    CONFIG_NAME = '.intexration'

    DIR = 'dir'
    IDX = 'idx'
    BIB = 'bib'

    def __init__(self, path):
        self.path = os.path.join(path, self.CONFIG_NAME)
        if not os.path.exists(path):
            raise RuntimeError("InTeXration config file not found")
        self.parser = configparser.ConfigParser()
        self.parser.read(self.path)

    def names(self):
        return self.parser.sections()

    def tex(self, name):
        if name not in self.names():
            raise RuntimeError("The request tex file does not exist")
        return name + '.tex'

    def dir(self, name):
        if self.parser.has_option(name, self.DIR):
            return self.parser[name][self.DIR]
        return ''

    def idx(self, name):
        if self.parser.has_option(name, self.IDX):
            return self.parser[name][self.IDX]
        return name + '.idx'

    def bib(self, name):
        if self.parser.has_option(name, self.BIB):
            return self.parser[name][self.BIB]
        return name


class RunArgumentParser:

    def __init__(self, arguments, config):
        self.arguments = arguments
        self.config = config
        self.exit = False

    def get(self, argument):
        return getattr(self.arguments, argument)

    def is_set(self, argument):
        return hasattr(self.arguments, argument) and getattr(self.arguments, argument) is not None

    def is_true(self, argument):
        return hasattr(self.arguments, argument) and hasattr(self.arguments, argument)

    def parse(self):
        self._parse_config()
        self._parse_api()
        self._exit()

    def _parse_config(self):
        if self.is_set('config_host'):
            self.config.write('SERVER', 'host', self.get('config_host'))
            self._exit_on_finish()
        if self.is_set('config_port'):
            self.config.write('SERVER', 'port', self.get('config_port'))
            self._exit_on_finish()
        if self.is_set('config_export'):
            self.config.file_export(self.get('config_export'))
            self._exit_on_finish()
        if self.is_set('config_import'):
            self.config.file_import(self.get('config_import'))
            self._exit_on_finish()

    def _parse_api(self):
        api_manager = ApiManager()
        if self.is_set('api_add'):
            api_manager.add_key(self.get('api_add'))
            self._exit_on_finish()
        if self.is_set('api_remove'):
            api_manager.remove_key(self.get('api_remove'))
            self._exit_on_finish()
        if self.is_true('api_list'):
            for line in api_manager.all_keys():
                print(line[0])
            self._exit_on_finish()
        if self.is_set('api_export'):
            api_manager.export_file(self.get('api_export'))
            self._exit_on_finish()
        if self.is_set('api_import'):
            api_manager.import_file(self.get('api_import'))
            self._exit_on_finish()

    def _exit_on_finish(self):
        self.exit = True

    def _exit(self):
        if self.exit:
            sys.exit(0)