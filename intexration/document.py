import os
import shutil


class Document:

    PDF_EXTENSION = '.pdf'
    LOG_EXTENSION = '.log'

    SEPARATOR = '/'
    NEWLINE = '\n'
    ERROR = ' !'
    WARMING = 'Warning'

    def __init__(self, name, path):
        self.path = path
        self.pdf = name + self.PDF_EXTENSION
        self.log = name + self.LOG_EXTENSION
        if not self.exist():
            raise RuntimeError("The document files do not exist")
        self._lines = self._read_log()

    def __set__(self, instance, path):
        if not os.path.exists(path):
            raise RuntimeError('The document path does not exist')
        else:
            self.path = path

    def path_pdf(self):
        return os.path.join(self.path, self.pdf)

    def path_log(self):
        return os.path.join(self.path, self.log)

    def exist(self):
        return os.path.exists(self.path_pdf()) and os.path.exists(self.path_log())

    def move_to(self, path):
        # Current Paths
        old_pdf = self.path_pdf()
        old_log = self.path_log()
        # New Paths
        self.path = path
        new_pdf = self.path_pdf()
        new_log = self.path_log()
        # Move All
        shutil.move(old_pdf, new_pdf)
        shutil.move(old_log, new_log)

    def _read_log(self):
        """Read all lines form log file"""
        path = self.path_log()
        log_file = open(path, "r", encoding='latin-1')
        return log_file.readlines()

    def warnings(self):
        """Parse warnings from log file."""
        warnings = []
        multi_line_error = False
        for line in self._lines:
            if multi_line_error and line == self.NEWLINE:
                multi_line_error = False
            if self.WARMING in line or multi_line_error:
                warnings.append(line)
                multi_line_error = True
        return warnings

    def errors(self):
        """Parse errors from logfile."""
        errors = []
        multi_line_error = False
        for line in self._lines:
            if multi_line_error and line == self.NEWLINE:
                multi_line_error = False
            if line.startswith(self.ERROR) or multi_line_error:
                errors.append(line.replace(self.ERROR, ""))
                multi_line_error = True
        return errors

    def logs(self):
        return self._lines