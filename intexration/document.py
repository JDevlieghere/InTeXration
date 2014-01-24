import logging
import os
from intexration.intexration import IntexrationConfig


class Document:
    def __init__(self, name, root):
        self.name = name
        self.root = root
        self._lines = self._read_log()
        self.config = IntexrationConfig.Instance()

    def log_name(self):
        return self.name + '.log'

    def log_path(self):
        return os.path.join(self.root, self.log_name())

    def pdf_name(self):
        return self.name + '.pdf'

    def pdf_path(self):
        return os.path.join(self.root, self.pdf_name())

    def _read_log(self):
        """Read all lines form log file"""
        path = self.log_path()
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
            if multi_line_error and line == self.config.constant('newline'):
                multi_line_error = False
            if self.config.constant('latex_warning') in line or multi_line_error:
                warnings.append(line)
                multi_line_error = True
        return warnings

    def get_errors(self):
        """Parse errors from logfile."""
        errors = []
        multi_line_error = False
        for line in self._lines:
            if multi_line_error and line == self.config.constant('newline'):
                multi_line_error = False
            if line.startswith(self.config.constant('latex_error')) or multi_line_error:
                errors.append(line.replace(self.config.constant('latex_error'), ""))
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