import configparser
import os

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