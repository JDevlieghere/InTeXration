import configparser
import contextlib
import logging
import os
import errno
import shutil
import subprocess
from intexration import config


@contextlib.contextmanager
def cd(dirname):
    cur_dir = config.PATH_ROOT
    try:
        os.chdir(dirname)
        yield
    finally:
        os.chdir(cur_dir)


class Task:
    def __init__(self, url, repository, owner, commit):
        self._url = url
        self._repository = repository
        self._owner = owner
        self._commit = commit
        self._build_dir = self._create_dir(config.PATH_BUILD, commit)
        self._output_dir = self._create_dir(config.PATH_OUT)

    def _create_dir(self, root, suffix=''):
        """Safely create a directory."""
        path = os.path.join(root, self._owner, self._repository, suffix)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path

    def _clone(self):
        """Clone repository to build dir."""
        if subprocess.call(['git', 'clone', self._url, self._build_dir], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) != 0:
            raise RuntimeError('git clone failed!')
        logging.debug("Cloned %s", self._repository)

    def _makeindex(self, document):
        """Make index."""
        working_dir = os.path.join(self._build_dir, document.subdir)
        with cd(working_dir):
            if subprocess.call(['makeindex', document.idx], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s:Makeindex failed.", self._repository)

    def _bibtex(self, document):
        """Compile bibtex."""
        working_dir = os.path.join(self._build_dir, document.subdir)
        with cd(working_dir):
            if subprocess.call(['bibtex', document.bib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s:Bibtex failed.", self._repository)

    def _compile(self, document):
        """Compile with pdflatex."""
        working_dir = os.path.join(self._build_dir, document.subdir)
        with cd(working_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', document.tex], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.error("%s:Compilation (pdflatex) finished with errors.", self._repository)

    def _copy(self, document):
        """Copy the PDF and Logfile to the output directory."""
        working_dir = os.path.join(self._build_dir, document.subdir)
        # PDF File
        pdf_source_path = os.path.join(working_dir, document.pdf)
        pdf_dest_path = os.path.join(self._output_dir, document.pdf)
        shutil.copyfile(pdf_source_path, pdf_dest_path)
        # Log File
        log_source_path = os.path.join(working_dir, document.log)
        log_dest_path = os.path.join(self._output_dir, document.log)
        shutil.copyfile(log_source_path, log_dest_path)

    def _clean(self):
        """Clean the build directory."""
        shutil.rmtree(self._build_dir)
        logging.debug("Directory %s cleaned.", self._build_dir)

    def _build(self, document):
        """Build all."""
        self._compile(document)
        self._makeindex(document)
        self._bibtex(document)
        self._compile(document)
        self._copy(document)

    def run(self):
        """Execute this task"""
        logging.info("New InTeXRation task started for %s", self._repository)
        try:
            self._clone()
        except Exception as e:
            logging.error(e)
        path = os.path.join(self._build_dir, '.intexration')
        parser = DocumentParser(path)
        for build in parser.documents():
            try:
                self._build(build)
            except Exception as e:
                logging.error(e)
        self._clean()
        logging.info("Task finished for %s.", self._repository)


class BuildDocument:
    def __init__(self, name, subdir, idx, bib):
        self.subdir = subdir
        self.idx = idx + '.idx'
        self.bib = bib
        self.tex = name + '.tex'
        self.pdf = name + '.pdf'
        self.log = name + '.log'


class DocumentParser:
    def __init__(self, path):
        self._path = path

    def documents(self):
        """Return all builds from the .intexration file."""
        documents = []
        if os.path.exists(self._path):
            parser = configparser.ConfigParser()
            parser.read(self._path)
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
            logging.error("No .intexration file found!")
        return documents