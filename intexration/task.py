import contextlib
import logging
import os
import errno
import shutil
import subprocess
from intexration import config
from intexration.document import DocumentParser


@contextlib.contextmanager
def cd(dirname):
    cur_dir = config.PATH_ROOT
    try:
        os.chdir(dirname)
        yield
    finally:
        os.chdir(cur_dir)


class Task:
    def __init__(self, repository, owner, commit):
        self._owner = owner
        self._repository = repository
        self.build_dir = self._create_dir(config.PATH_BUILD,  commit)
        self.output_dir = self._create_dir(config.PATH_OUTPUT)

    def url(self):
        return 'https://github.com/' + self._owner + '/' + self._repository + '.git'

    def _create_dir(self, root, commit=''):
        """Safely create a directory."""
        path = os.path.join(root, self._owner, self._repository, commit)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path

    def title(self):
        return self._owner+'/'+self._repository

    def _clone(self):
        """Clone repository to build dir."""
        if subprocess.call(['git', 'clone',  self.url(), self.build_dir], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) != 0:
            logging.error("Clone failed for %s", self.title())
        logging.info("Cloned %s", self.title())

    def _makeindex(self, document):
        """Make index."""
        working_dir = os.path.join(self.build_dir, document.subdir)
        with cd(working_dir):
            if subprocess.call(['makeindex', document.idx], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Makeindex failed  for %s", self.title())

    def _bibtex(self, document):
        """Compile bibtex."""
        working_dir = os.path.join(self.build_dir, document.subdir)
        with cd(working_dir):
            if subprocess.call(['bibtex', document.bib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning("Bibtex failed for %s", self.title())

    def _compile(self, document):
        """Compile with pdflatex."""
        working_dir = os.path.join(self.build_dir, document.subdir)
        with cd(working_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', document.tex], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Compilation finished with errors for %s", self.title())

    def _copy(self, document):
        """Copy the PDF and log to the output directory."""
        working_dir = os.path.join(self.build_dir, document.subdir)
        # PDF File
        pdf_source_path = os.path.join(working_dir, document.pdf)
        pdf_dest_path = os.path.join(self.output_dir, document.pdf)
        shutil.copyfile(pdf_source_path, pdf_dest_path)
        # Log File
        log_source_path = os.path.join(working_dir, document.log)
        log_dest_path = os.path.join(self.output_dir, document.log)
        shutil.copyfile(log_source_path, log_dest_path)

    def _clean(self):
        """Clean the build directory."""
        shutil.rmtree(self.build_dir)

    def _build(self, document):
        """Build all."""
        self._compile(document)
        self._makeindex(document)
        self._bibtex(document)
        self._compile(document)
        self._copy(document)

    def run(self):
        """Execute this task"""
        logging.info("Task created for %s", self.title())
        try:
            self._clone()
        except Exception as e:
            logging.error(e)
        parser = DocumentParser(self)
        for build in parser.documents():
            try:
                self._build(build)
            except Exception as e:
                logging.error(e)
        self._clean()
        logging.info("Task finished for %s", self.title())

