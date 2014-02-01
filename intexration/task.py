import configparser
import logging
import os
import shutil
import subprocess
from threading import Thread
from intexration import constants
from intexration.tools import cd, create_dir, remove, empty


class Task:

    def run(self):
        pass


class CompileTask(Task):

    MAKEINDEX = 'makeindex'
    BIBTEX = 'bibtex'
    PDFLATEX = 'pdflatex'

    def __init__(self, input_dir, output_dir, document):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.document = document

    def _makeindex(self):
        """Make index."""
        with cd(self.input_dir):
            if subprocess.call([self.MAKEINDEX, self.document.idx],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Makeindex failed for %s", self.document.name)

    def _bibtex(self):
        """Compile bibtex."""
        with cd(self.input_dir):
            if subprocess.call([self.BIBTEX, self.document.bib],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Bibtex failed for %s", self.document.name)

    def _compile(self):
        """Compile with pdflatex."""
        with cd(self.input_dir):
            if subprocess.call([self.PDFLATEX, '-interaction=nonstopmode', self.document.tex],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Compilation finished with errors for %s", self.document.name)

    def _copy(self):
        """Copy the PDF and log to the output directory."""
        pdf_source_path = os.path.join(self.input_dir, self.document.pdf)
        pdf_dest_path = os.path.join(self.output_dir, self.document.pdf)
        shutil.copyfile(pdf_source_path, pdf_dest_path)
        log_source_path = os.path.join(self.input_dir, self.document.log)
        log_dest_path = os.path.join(self.output_dir, self.document.log)
        shutil.copyfile(log_source_path, log_dest_path)

    def run(self):
        logging.info("Compiling %s", self.document.name)
        self._compile()
        self._makeindex()
        self._bibtex()
        self._compile()
        self._copy()


class BuildConfigParser:

    DIR = 'dir'
    IDX = 'idx'
    BIB = 'bib'

    def __init__(self, build):
        path = os.path.join(build.clone_dir, build.CONFIG_NAME)
        if not os.path.exists(path):
            raise RuntimeError("InTeXration config file not found")
        self.build = build
        self.parser = configparser.ConfigParser()
        self.parser.read(path)

    def parse(self):
        for name in self._names():
            document = Document(name, self._dir(name), self._idx(name), self._bib(name))
            self.build.add_document(document)

    def _names(self):
        return self.parser.sections()

    def _dir(self, name):
        if self.parser.has_option(name, self.DIR):
            return self.parser[name][self.DIR]
        return ''

    def _idx(self, name):
        if self.parser.has_option(name, self.IDX):
            return self.parser[name][self.IDX]
        return name + '.idx'

    def _bib(self, name):
        if self.parser.has_option(name, self.BIB):
            return self.parser[name][self.BIB]
        return name


class IntexrationTask(Task):

    def __init__(self, build, threaded=True):
        self.build = build
        self.threaded = threaded
        self.config = BuildConfigParser(build)

    def run(self):
        if self.threaded:
            logging.info("Threaded compilation task started")
        else:
            logging.info("Compilation task started")
        threads = []
        self.config.parse()
        for document in self.build.documents:
            task_input = os.path.join(self.build.clone_dir, document.directory)
            task = CompileTask(task_input, self.build.output_dir, document)
            if self.threaded:
                threads.append(Thread(target=task.run))
            else:
                task.run()
        # Start all threads
        [t.start() for t in threads]
        # Join all threads
        [t.join() for t in threads]


class CloneTask(Task):

    def __init__(self, build):
        self.build = build

    def _clean(self):
        remove(self.build.clone_dir)

    def _clone(self):
        """Clone repository to build dir."""
        logging.info("Cloning from %s", self.build.url)
        if subprocess.call(['git', 'clone',  self.build.url, self.build.clone_dir]) != 0:
            raise RuntimeError("Clone failed")

    def run(self):
        self._clean()
        self._clone()


class Document:

    TEX_EXTENSION = 'tex'
    PDF_EXTENSION = 'pdf'
    LOG_EXTENSION = 'log'

    def __init__(self, name, directory, idx, bib):
        self.name = name
        self.directory = directory
        self.idx = idx
        self.bib = bib
        self.tex = self.add_extension(name, self.TEX_EXTENSION)
        self.pdf = self.add_extension(name, self.PDF_EXTENSION)
        self.log = self.add_extension(name, self.LOG_EXTENSION)

    @staticmethod
    def add_extension(name, extension):
        return name + '.' + extension

    def __str__(self):
        return self.name


class Build:

    SEPARATOR = '/'
    CONFIG_NAME = '.intexration'

    def __init__(self, url, owner, repository, commit):
        self.url = self.convert(url)
        self.owner = owner
        self.repository = repository
        self.commit = commit
        self.documents = []
        self.input_dir = create_dir(os.path.join(constants.DIRECTORY_ROOT,
                                                 constants.DIRECTORY_TEMP))
        self.clone_dir = os.path.join(self.input_dir,
                                      self.owner,
                                      self.repository,
                                      self.commit)
        self.output_dir = create_dir(os.path.join(constants.DIRECTORY_ROOT,
                                                  constants.DIRECTORY_OUTPUT,
                                                  self.owner,
                                                  self.repository))

    def add_document(self, document):
        self.documents.append(document)

    @staticmethod
    def convert(url):
        if 'https://' in url:
            return url + '.git'
        return url

    def __str__(self):
        return self.owner + self.SEPARATOR + self.repository


class BuildTask:

    def __init__(self, build, threaded=True):
        self.build = build
        self.threaded = threaded

    def run(self):
        logging.info("Build started for %s", self.build)
        clone_task = CloneTask(self.build)
        try:
            clone_task.run()
            IntexrationTask(self.build, self.threaded).run()
        except RuntimeError as e:
            logging.error(e)
        # finally:
        #     remove(self.build.clone_dir)
        logging.info("Build finished for %s", self.build)