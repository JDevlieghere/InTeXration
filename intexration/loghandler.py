# Logger
import os


class LogHandler:
    def __init__(self, path):
        self._path = path

    def _lines(self):
        if not os.path.isfile(self._path):
            raise RuntimeError("The logfile does not exist")
        log_file = open(self._path, "r", encoding='latin-1')
        return log_file.readlines()

    def get_warnings(self):
        warning_prefix = 'Warning'
        errors = []
        multi_line_error = False
        for line in self._lines():
            if multi_line_error and line == '\n':
                multi_line_error = False
            if warning_prefix in line or multi_line_error:
                errors.append(line.replace(error_prefix, ""))
                multi_line_error = True
        return errors

    def get_errors(self):
        error_prefix = "! "
        errors = []
        multi_line_error = False
        for line in self._lines():
            if multi_line_error and line == '\n':
                multi_line_error = False
            if line.startswith(error_prefix) or multi_line_error:
                errors.append(line.replace(error_prefix, ""))
                multi_line_error = True
        return errors

    def get_all(self):
        return self._lines()