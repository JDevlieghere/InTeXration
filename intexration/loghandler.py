# Logger
import logging
import os

logger = logging.getLogger('intexration')


class LogHandler:
    def __init__(self, path):
        self._path = path

    def _lines(self):
        if not os.path.isfile(self._path):
            raise RuntimeError("The logfile does not exist")
        log_file = open(self._path, "r", encoding='latin-1')
        return log_file.readlines()

    def get_errors(self):
        error_prefix = "! "
        errors = []
        for line in self._lines():
            if line.startswith(error_prefix):
                errors.append(line.replace(error_prefix, ""))
        return errors

    def get_all(self):
        return self._lines()