import configparser
import logging
import os
from intexration import config

__author__ = 'Jonas'


class BuildDocument:
    def __init__(self, name, subdir, idx, bib):
        self.subdir = subdir
        self.idx = idx + '.idx'
        self.bib = bib
        self.tex = name + '.tex'
        self.pdf = name + '.pdf'
        self.log = name + '.log'


class DocumentParser:
    def __init__(self, task):
        self._task = task

    def documents(self):
        """Return all builds from the .intexration file."""
        path = os.path.join(self._task.build_dir, '.intexration')
        documents = []
        if os.path.exists(path):
            parser = configparser.ConfigParser()
            parser.read(path)
            for build_name in parser.sections():
                if parser.has_option(build_name, 'dir'):
                    subdir = parser[build_name]['dir']
                else:
                    subdir = ''
                if parser.has_option(build_name, 'idx'):
                    idx = parser[build_name]['idx']
                else:
                    idx = build_name
                if parser.has_option(build_name, 'bib'):
                    bib = parser[build_name]['bib']
                else:
                    bib = build_name
                documents.append(BuildDocument(build_name, subdir, idx, bib))
        else:
            logging.error("No .intexration file found for %s", self._task.title())
        return documents


class Document:
    def __init__(self, name, root):
        self.name = name
        self.root = root
        self._lines = self._read_log()

    def log_name(self):
        return self.name + '.log'

    def log_file(self):
        return os.path.join(self.root, self.log_name())

    def pdf_name(self):
        return self.name + '.pdf'

    def pdf_file(self):
        return os.path.join(self.root, self.pdf_name())

    def _read_log(self):
        """Read all lines form log file"""
        path = self.log_file()
        if not os.path.exists(path):
            logging.error("Log file not found at %s", path)
            raise RuntimeWarning("Log file not found at %s", path)
        log_file = open(path, "r", encoding='latin-1')
        return log_file.readlines()

    def get_warnings(self):
        """Parse warnings from log file."""
        warnings = []
        multi_line_error = False
        for line in self._lines:
            if multi_line_error and line == config.LOG_NEW_LINE_CHAR:
                multi_line_error = False
            if config.LOG_WARNING_STRING in line or multi_line_error:
                warnings.append(line)
                multi_line_error = True
        return warnings

    def get_errors(self):
        """Parse errors from logfile."""
        errors = []
        multi_line_error = False
        for line in self._lines:
            if multi_line_error and line == config.LOG_NEW_LINE_CHAR:
                multi_line_error = False
            if line.startswith(config.LOG_ERROR_STRING) or multi_line_error:
                errors.append(line.replace(config.LOG_ERROR_STRING, ""))
                multi_line_error = True
        return errors

    def get_log(self):
        return self._lines


class DocumentExplorer:
    def __init__(self, root):
        self.root = root

    def all_owners(self):
        return os.listdir(self.root)

    def all_repos(self, owner):
        return os.listdir(os.path.join(self.root, owner))

    def all_names(self, owner, repo):
        names = []
        for file in os.listdir(os.path.join(self.root, owner, repo)):
            if file.endswith('.log'):
                names.append(file.replace('.log',''))
        return names

    def all_documents(self):
        documents = []
        for owner in self.all_owners():
            for repo in self.all_repos(owner):
                for name in self.all_names(owner, repo):
                    path = os.path.join(self.root, owner, repo)
                    documents.append(Document(name, path))
        return documents