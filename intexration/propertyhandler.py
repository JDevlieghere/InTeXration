import configparser
import os


class Build:
    def __init__(self, name, idx, bib):
        self._name = name
        self._idx = idx
        self._bib = bib

    def get_name(self):
        return self._name

    def get_idx(self):
        return self._idx

    def get_bib(self):
        return self._bib

    def get_tex(self):
        return self._name + '.tex'

    def get_pdf(self):
        return self._name + '.pdf'

    def get_log(self):
        return self._name + '.log'


class PropertyHandler:
    def __init__(self, path):
        self._path = path

    def get_builds(self):
        builds = []
        if os.path.exists(self._path):
            parser = configparser.ConfigParser()
            parser.read(self._path)
            for build_name in parser.sections():
                if parser.has_option(build_name, 'idx'):
                    idx = parser[build_name]['idx']
                else:
                    idx = build_name + '.idx'
                if parser.has_option(build_name, 'bib'):
                    bib = parser[build_name]['bib']
                else:
                    bib = build_name
                builds.append(Build(build_name, idx, bib))
        return builds