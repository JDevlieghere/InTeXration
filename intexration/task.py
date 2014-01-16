import configparser
import contextlib
import logging
import os
import errno
import shutil
import subprocess


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
        if subprocess.call(['git', 'clone', self._url, self._build_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            raise RuntimeError('git clone failed!')
        logging.debug("Cloned %s to &s", self._repository, self._build_dir)

    def _makeindex(self, file):
        with cd(self._build_dir):
            if subprocess.call(['makeindex', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s:Makeindex failed.", self._repository)

    def _bibtex(self, file):
        with cd(self._build_dir):
            if subprocess.call(['bibtex', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s:Bibtex failed.", self._repository)

    def _compile(self, file):
        with cd(self._build_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', file], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.error("%s:Compilation (pdflatex) finished with errors.", self._repository)

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
        logging.debug("Directory %s cleaned.", self._build_dir)

    def _build(self, name, idx, bib):
        tex = name + '.tex'
        pdf = name + '.pdf'
        log = name + '.log'
        self._compile(tex)
        self._makeindex(idx)
        self._bibtex(bib)
        self._compile(tex)
        self._copy(pdf, log)

    def run(self):
        logging.info("New InTeXRation task started for %s", self._repository)
        try:
            self._clone()
        except Exception as e:
            logging.error(e)
        path = os.path.join(self._build_dir, '.intexration')
        if os.path.exists(path):
            parser = configparser.ConfigParser()
            parser.read(path)
            for build_name in parser.sections():
                idx = build_name + '.idx'
                bib = build_name + '.bib'
                try:
                    self._build(build_name, idx, bib)
                except Exception as e:
                    logging.error(e)
        else:
            logging.error("No .intexration file found for %s.", self._repository)
        self._clean()
        logging.info("Task finished for %s.", self._repository)