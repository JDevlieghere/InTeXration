import contextlib
import os
import errno
import shutil
import subprocess
import sys


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

    def _compile(self, file):
        @contextlib.contextmanager
        def cd(dirname):
            cur_dir = os.getcwd()
            try:
                os.chdir(dirname)
                yield
            finally:
                os.chdir(cur_dir)

        output_path = self._output_dir
        with cd(self._build_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', '-aux-directory=' + output_path,
                                '-output-directory=' + output_path, file]) != 0:
                raise RuntimeError('pdflatex compilation failed!')

    def _clean(self):
        shutil.rmtree(self._build_dir)

    def run(self):
        def error(*objs):
            print("ERROR: ", *objs, end='\n', file=sys.stderr)
        try:
            self._clone()
            self._compile('main.tex')
            # Run twice for cross-references
            self._compile('main.tex')
        except Exception as e:
            error(e)
        finally:
            self._clean()


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
                while line != "":
                    errors.append(line.replace(error_prefix, ""))
        return errors

    def get_wanrings(self):
        return ''

    def get_all(self):
        return self._lines()