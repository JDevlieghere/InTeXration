import configparser
import csv
import logging
import os
from intexration import config


class Build:
    def __init__(self, name, dir, idx, bib):
        self._name = name
        self._dir = dir
        self._idx = idx
        self._bib = bib

    def get_name(self):
        return self._name

    def get_dir(self):
        return self._dir

    def get_idx(self):
        return self._idx + '.idx'

    def get_bib(self):
        return self._bib

    def get_tex(self):
        return self._name + '.tex'

    def get_pdf(self):
        return self._name + '.pdf'

    def get_log(self):
        return self._name + '.log'


class LogHelper:
    def __init__(self, path):
        self._lines = self._read_lines(path)

    @staticmethod
    def _read_lines(path):
        """Read all lines form log file"""
        if not os.path.exists(path):
            raise RuntimeError("The logfile does not exist")
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

    def get_all(self):
        return self._lines


class ApiHelper:
    def __init__(self, path):
        self._path = path

    def is_valid(self, key_to_check):
        with open(self._path, newline='') as key_file:
            key_reader = csv.reader(key_file, delimiter=',')
            for row in key_reader:
                if key_to_check in row:
                    return True
        return False

    def add(self, api_key):
        with open(self._path, 'a', newline='') as key_file:
            key_writer = csv.writer(key_file, delimiter=',', quoting=csv.QUOTE_NONE)
            key_writer.writerow([api_key])

    def get_all(self):
        key_file = open(self._path, 'r', newline='')
        rows = list(csv.reader(key_file, delimiter=','))
        key_file.close()
        return rows

    def remove(self, api_key):
        rows = []
        for row in self.get_all():
            if api_key not in row:
                rows.append(row)
        with open(self._path, 'w', newline='') as key_file:
            key_writer = csv.writer(key_file, delimiter=',')
            for row in rows:
                key_writer.writerow(row)
