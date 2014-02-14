import logging
import os
import shutil
import subprocess
import tempfile
from intexration.tools import create_dir, cd
from intexration.build import Identifier, Build
from intexration.document import Document
from intexration.parser import BuildParser


class Task():

    def run(self):
        pass


class CloneTask(Task):

    def __init__(self, manager, request):
        self.build_manager = manager
        self.build_request = request
        self.temp_directory = tempfile.mkdtemp()
        self.clone_directory = self._create_dir()

    def _create_dir(self):
        return create_dir(os.path.join(self.temp_directory,
                                       self.build_request.owner,
                                       self.build_request.repository,
                                       self.build_request.commit))

    def _clone(self):
        logging.info("Cloning to %s", self.clone_directory)
        if subprocess.call(['git', 'clone',  self.build_request.https_url(), self.clone_directory],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0:
            return
        if subprocess.call(['git', 'clone',  self.build_request.ssh_url(), self.clone_directory],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0:
            return
        raise RuntimeError("Clone failed: both https and ssh cloning failed.")

    def _submit_builds(self):
        builds = dict()
        build_parser = BuildParser(self.clone_directory)
        for name in build_parser.names():
            identifier = Identifier(self.build_request.owner,
                                    self.build_request.repository,
                                    name)
            src_path = os.path.join(self.clone_directory, build_parser.dir(name))
            dst_path = os.path.join(self.temp_directory, name)
            shutil.copytree(src_path, dst_path)
            build = Build(dst_path,
                          build_parser.tex(name),
                          build_parser.idx(name),
                          build_parser.bib(name))
            builds[identifier] = build
        self.build_manager.submit_builds(builds)

    def _clean(self):
        shutil.rmtree(self.clone_directory)

    def run(self):
        try:
            self._clone()
            self._submit_builds()
            self._clean()
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
        return create_dir(os.path.join(self.build_manager.output,
                                       self.identifier.owner,
                                       self.identifier.repository))

    def _makeindex(self):
        """Make index."""
        with cd(self.build.path):
            if subprocess.call([self.MAKEINDEX, self.build.idx],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s Makeindex failed for %s", self.identifier, self.build.idx)

    def _bibtex(self):
        """Compile bibtex."""
        with cd(self.build.path):
            if subprocess.call([self.BIBTEX, self.build.bib],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s Bibtex failed for %s", self.identifier, self.build.bib)

    def _compile(self):
        """Compile with pdflatex."""
        with cd(self.build.path):
            if subprocess.call([self.PDFLATEX, '-interaction=nonstopmode', self.build.tex],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("%s Compilation finished with errors for %s", self.identifier, self.build.tex)

    def _submit_documents(self):
        document = Document(self.identifier.name, self.build.path)
        document.move_to(self.document_directory)
        self.build_manager.submit_document(self.identifier, document)
        self.build.finish()

    def run(self):
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
