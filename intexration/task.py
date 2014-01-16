import contextlib
import logging
import os
import errno
import shutil
import subprocess

# Logger
logger = logging.getLogger('intexration')

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
        logger.debug("Cloned %s to &s", self._repository, self._build_dir)

    def _makeindex(self, file):
        with cd(self._build_dir):
            if subprocess.call(['makeindex', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logger.warning('Makeindex failed.')

    def _bibtex(self, file):
        with cd(self._build_dir):
            if subprocess.call(['bibtex', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logger.warning('Bibtex failed.')

    def _compile(self, file):
        with cd(self._build_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', file], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logger.error('Compilation (pdflatex) finished with errors.')

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
        logger.debug("Directory %s cleaned.", self._build_dir)

    def run(self):
        logger.info("New InTeXRation task started for %s", self._repository)
        try:
            self._clone()
            self._compile('main.tex')
            self._makeindex('main.idx')
            self._bibtex('main')
            self._compile('main.tex')
            self._copy('main.pdf', 'main.log')
        except Exception as e:
            logger.error(e)
        finally:
            self._clean()
        logger.info("Task finished for " + self._repository)