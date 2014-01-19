import contextlib
import logging
import os
import errno
import shutil
import subprocess

# Context Swtich
from intexration import config
from intexration.helper import BuildHelper


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
        self._repository = self._convert(repository)
        self._owner = owner
        self._commit = commit
        self._build_dir = self._create_dir('build', commit)
        self._output_dir = self._create_dir('out')

    def _create_dir(self, prefix, suffix=''):
        """Safely create a directory."""
        path = os.path.join(config.PATH_ROOT, prefix, self._owner, self._repository, suffix)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path

    @staticmethod
    def _convert(url):
        """Add .git extenions to repository URL."""
        if url.startswith('https://'):
            return url + '.git'
        return url

    def _clone(self):
        """Clone repository to build dir."""
        if subprocess.call(['git', 'clone', self._url, self._build_dir], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) != 0:
            raise RuntimeError('git clone failed!')
        logging.debug("Cloned %s", self._repository)

    def _makeindex(self, file):
        """Make index."""
        with cd(self._build_dir):
            if subprocess.call(['makeindex', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s:Makeindex failed.", self._repository)

    def _bibtex(self, file):
        """Compile bibtex."""
        with cd(self._build_dir):
            if subprocess.call(['bibtex', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s:Bibtex failed.", self._repository)

    def _compile(self, file):
        """Compile with pdflatex."""
        with cd(self._build_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', file], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.error("%s:Compilation (pdflatex) finished with errors.", self._repository)

    def _move(self, dir, tex_file, idx_file, bib_file):
        """Copy the source files to the root of the build directory."""
        # TeX file
        tex_source_path = os.path.join(self._build_dir, dir, tex_file)
        tex_dest_path = os.path.join(self._build_dir, tex_file)
        shutil.copyfile(tex_source_path, tex_dest_path)
        # idx File
        try:
            idx_source_path = os.path.join(self._build_dir, dir, idx_file)
            idx_dest_path = os.path.join(self._build_dir, idx_file)
            shutil.copyfile(idx_source_path, idx_dest_path)
        except IOError:
            logging.debug("No index file to copy.")
        try:
            bib_source_path = os.path.join(self._build_dir, dir, bib_file)
            bib_dest_path = os.path.join(self._build_dir, bib_file)
            shutil.copyfile(bib_source_path, bib_dest_path)
        except IOError:
            logging.debug("No BibTex file to copy.")

    def _copy(self, pdf_file, log_file):
        """Copy the PDF and Logfile to the output directory."""
        # PDF File
        pdf_source_path = os.path.join(self._build_dir, pdf_file)
        pdf_dest_path = os.path.join(self._output_dir, pdf_file)
        shutil.copyfile(pdf_source_path, pdf_dest_path)
        # Log File
        log_source_path = os.path.join(self._build_dir, log_file)
        log_dest_path = os.path.join(self._output_dir, log_file)
        shutil.copyfile(log_source_path, log_dest_path)

    def _clean(self):
        """Clean the build directory."""
        shutil.rmtree(self._build_dir)
        logging.debug("Directory %s cleaned.", self._build_dir)

    def _build(self, build):
        """Build all."""
        if build.get_dir() != '':
            self._move(build.get_dir(), build.get_tex(), build.get_idx(), build.get_bib())
        self._compile(build.get_tex())
        self._makeindex(build.get_idx())
        self._bibtex(build.get_bib())
        self._compile(build.get_tex())
        self._copy(build.get_pdf(), build.get_log())

    def run(self):
        """Execute this task"""
        logging.info("New InTeXRation task started for %s", self._repository)
        try:
            self._clone()
        except Exception as e:
            logging.error(e)
        path = os.path.join(self._build_dir, '.intexration')
        property_handler = BuildHelper(path)
        for build in property_handler.get_builds():
            try:
                self._build(build)
            except Exception as e:
                logging.error(e)
        self._clean()
        logging.info("Task finished for %s.", self._repository)