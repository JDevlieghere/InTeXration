import contextlib
import logging
import os
import errno
import shutil
import subprocess
import sys

# Logger
logging.basicConfig()


# Context Swtich
@contextlib.contextmanager
def cd(dirname):
    cur_dir = os.getcwd()
    try:
        os.chdir(dirname)
        yield
    finally:
        os.chdir(cur_dir)


class Task:
    def __init__(self, url, repository, commit):
        self._url = url
        self._repository = self._convert(repository)
        self._commit = commit
        self._build_dir = self._create_dir('build', commit)
        self._output_dir = self._create_dir('out')

    def _create_dir(self, prefix, suffix=''):
        path = os.path.join(os.getcwd(), prefix, self._repository, suffix)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path

    @staticmethod
    def _convert(url):
        if url.startswith('https://'):
            return url + '.git'
        return url

    def _clone(self):
        if subprocess.call(['git', 'clone', self._url, self._build_dir]) != 0:
            raise RuntimeError('git clone failed!')

    def _makeindex(self, file):
        with cd(self._build_dir):
            if subprocess.call(['makeindex', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning('makeindex failed!')

    def _bibtex(self, file):
        with cd(self._build_dir):
            if subprocess.call(['bibtex', file]) != 0:
                logging.warning('bibtex failed!')

    def _compile(self, file):
        with cd(self._build_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', file], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning('pdflatex compilation finished with errors!')

    def _copy(self, pdf_file, log_file):
        # PDF File
        pdf_source_path = os.path.join(self._build_dir, pdf_file)
        pdf_dest_path = os.path.join(self._output_dir, pdf_file)
        shutil.copyfile(pdf_source_path, pdf_dest_path)
        # Log File
        log_source_path = os.path.join(self._build_dir, log_file)
        log_dest_path = os.path.join(self._output_dir, log_file)
        shutil.copyfile(log_source_path, log_dest_path)

    def _clean(self):
        shutil.rmtree(self._build_dir)

    def run(self):
        logging.info("Task started for " + self._repository)
        try:
            self._clone()
            self._compile('main.tex')
            self._makeindex('main.idx')
            self._bibtex('main.bib')
            self._compile('main.tex')
            self._copy('main.pdf', 'main.log')
        except Exception as e:
            logging.error(e)
        finally:
            self._clean()
        logging.info("Task finished for " + self._repository)


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

    def get_wanrings(self):
        return ''

    def get_all(self):
        return self._lines()