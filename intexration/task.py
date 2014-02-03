import configparser
import logging
import os
import subprocess
import tempfile
from intexration.tools import create_dir, cd
from intexration import constants
from intexration.build import Identifier, Build
from intexration.document import Document


class Task():

    def run(self):
        pass


class BuildParser:

    CONFIG_NAME = '.intexration'

    DIR = 'dir'
    IDX = 'idx'
    BIB = 'bib'

    def __init__(self, path):
        self.path = os.path.join(path, self.CONFIG_NAME)
        if not os.path.exists(path):
            raise RuntimeError("InTeXration config file not found")
        self.parser = configparser.ConfigParser()
        self.parser.read(self.path)

    def names(self):
        return self.parser.sections()

    def tex(self, name):
        if name not in self.names():
            raise RuntimeError("The request tex file does not exist")
        return name + '.tex'

    def dir(self, name):
        if self.parser.has_option(name, self.DIR):
            return self.parser[name][self.DIR]
        return ''

    def idx(self, name):
        if self.parser.has_option(name, self.IDX):
            return self.parser[name][self.IDX]
        return name + '.idx'

    def bib(self, name):
        if self.parser.has_option(name, self.BIB):
            return self.parser[name][self.BIB]
        return name


class CloneTask(Task):

    def __init__(self, manager, request):
        self.build_manager = manager
        self.build_request = request
        self.build_directory = self._create_dir()

    def _create_dir(self):
        temp_directory = tempfile.mkdtemp()
        return create_dir(os.path.join(temp_directory,
                                       self.build_request.owner,
                                       self.build_request.repository,
                                       self.build_request.commit))

    def _clone(self):
        logging.info("Cloning to %s", self.build_directory)
        if subprocess.call(['git', 'clone',  self.build_request.url, self.build_directory],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) != 0:
            raise RuntimeError("Clone failed")

    def _submit_builds(self):
        builds = dict()
        build_parser = BuildParser(self.build_directory)
        for name in build_parser.names():
            identifier = Identifier(self.build_request.owner,
                                    self.build_request.repository,
                                    name)
            path = os.path.join(self.build_directory, build_parser.dir(name))
            build = Build(path,
                          build_parser.tex(name),
                          build_parser.idx(name),
                          build_parser.bib(name))
            builds[identifier] = build
        self.build_manager.submit_builds(builds)

    def run(self):
        try:
            self._clone()
            self._submit_builds()
        except RuntimeError as e:
            logging.error(e)
        except RuntimeWarning as e:
            logging.warning(e)

class CompileTask(Task):

    MAKEINDEX = 'makeindex'
    BIBTEX = 'bibtex'
    PDFLATEX = 'pdflatex'

    def __init__(self, manager, identifier, build):
        self.build_manager = manager
        self.identifier = identifier
        self.build = build
        self.document_directory = self._create_dir()

    def _create_dir(self):
        return create_dir(os.path.join(constants.PATH_OUTPUT,
                                       self.identifier.owner,
                                       self.identifier.repository,
                                       self.identifier.name))

    def _makeindex(self):
        """Make index."""
        with cd(self.build.path):
            if subprocess.call([self.MAKEINDEX, self.build.idx],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Makeindex failed for %s", self.build.idx)

    def _bibtex(self):
        """Compile bibtex."""
        with cd(self.build.path):
            if subprocess.call([self.BIBTEX, self.build.bib],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Bibtex failed for %s", self.build.bib)

    def _compile(self):
        """Compile with pdflatex."""
        with cd(self.build.path):
            if subprocess.call([self.PDFLATEX, '-interaction=nonstopmode', self.build.tex],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Compilation finished with errors for %s", self.build.tex)

    def _submit_documents(self):
        document = Document(self.identifier.name, self.build.path)
        document.move_to(self.document_directory)
        self.build_manager.submit_document(self.identifier, document)
        #self.build.finish()

    def run(self):
        logging.info("Compiling %s", self.identifier)
        try:
            self._compile()
            self._makeindex()
            self._bibtex()
            self._compile()
            self._submit_documents()
        except RuntimeError as e:
            logging.error(e)
        except RuntimeWarning as e:
            logging.warning(e)
