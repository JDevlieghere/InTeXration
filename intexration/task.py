import configparser
import contextlib
import logging
import os
import shutil
import subprocess
import errno
from threading import Thread
from intexration.intexration import IntexrationConfig
from intexration.singleton import Singleton


@contextlib.contextmanager
def cd(directory):
    cur_dir = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cur_dir)


def create_dir(path):
    """Safely create a directory."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return path


def empty(path, files_only=True):
    if not os.path.exists(path):
        return
    for content in os.listdir(path):
        content_path = os.path.join(path, content)
        try:
            os.remove(content_path)
        except OSError:
            if not files_only:
                shutil.rmtree(content_path)
        except Exception as e:
            logging.error(e)


def remove(path):
    shutil.rmtree(path)


class CompileTask:
    def __init__(self, input_dir, output_dir, name, idx, bib):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.name = name
        self.idx = idx
        self.bib = bib
        self.tex = name + '.tex'
        self.pdf = name + '.pdf'
        self.log = name + '.log'

    def _makeindex(self):
        """Make index."""
        with cd(self.input_dir):
            if subprocess.call(['makeindex', self.idx], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Makeindex failed for %s", self.name)

    def _bibtex(self):
        """Compile bibtex."""
        with cd(self.input_dir):
            if subprocess.call(['bibtex', self.bib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                logging.warning("Bibtex failed for %s", self.name)

    def _compile(self):
        """Compile with pdflatex."""
        with cd(self.input_dir):
            if subprocess.call(['pdflatex', '-interaction=nonstopmode', self.tex], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) != 0:
                logging.warning("Compilation finished with errors for %s", self.name)

    def _copy(self):
        """Copy the PDF and log to the output directory."""
        pdf_source_path = os.path.join(self.input_dir, self.pdf)
        pdf_dest_path = os.path.join(self.output_dir, self.pdf)
        shutil.copyfile(pdf_source_path, pdf_dest_path)
        log_source_path = os.path.join(self.input_dir, self.log)
        log_dest_path = os.path.join(self.output_dir, self.log)
        shutil.copyfile(log_source_path, log_dest_path)

    def run(self):
        logging.info("Compiling %s", self.name)
        self._compile()
        self._makeindex()
        self._bibtex()
        self._compile()
        self._copy()


class IntexrationBuildConfig:

    dir_key = 'dir'
    idx_key = 'idx'
    bib_key = 'bib'

    def __init__(self, path):
        if not os.path.exists(path):
            raise RuntimeError("InTeXration config file not found")
        self.parser = configparser.ConfigParser()
        self.parser.read(path)

    def names(self):
        return self.parser.sections()

    def dir(self, name):
        if self.parser.has_option(name, self.dir_key):
            return self.parser[name][self.dir_key]
        return ''

    def idx(self, name):
        if self.parser.has_option(name, self.idx_key):
            return self.parser[name][self.idx_key]
        return name + '.idx'

    def bib(self, name):
        if self.parser.has_option(name, self.bib_key):
            return self.parser[name][self.bib_key]
        return name


class IntexrationTask:

    config_name = '.intexration'

    def __init__(self, input_dir, output_dir, threaded=True):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.threaded = threaded
        self.config = IntexrationBuildConfig(os.path.join(self.input_dir, self.config_name))

    def run(self):
        if self.threaded:
            logging.info("Threaded compilation task started")
        else:
            logging.info("Compilation task started")
        threads = []
        for name in self.config.names():
            task_input = os.path.join(self.input_dir, self.config.dir(name))
            task = CompileTask(task_input, self.output_dir, name, self.config.idx(name), self.config.bib(name))
            if self.threaded:
                threads.append(Thread(target=task.run))
            else:
                task.run()
        # Start all threads
        [t.start() for t in threads]
        # Join all threads
        [t.join() for t in threads]


    def run_only(self, name):
        if not name in self.config.names():
            raise RuntimeError("Build not in intexration config")
        task_input = os.path.join(self.input_dir, self.config.dir(name))
        CompileTask(task_input, self.output_dir, name, self.config.idx(name),
                    self.config.bib(name)).run()


class CloneTask:

    def __init__(self, root, url, owner, repository, commit):
        self.root = root
        self.url = self.convert(url)
        self.owner = owner
        self.repository = repository
        self.commit = commit

    @staticmethod
    def convert(url):
        if 'https://' in url:
            return url + '.git'
        return url

    def clone_dir(self):
        path = os.path.join(self.root, self.owner, self.repository, self.commit)
        return create_dir(path)

    def _clone(self):
        """Clone repository to build dir."""
        logging.info("Cloning from %s", self.url())
        if subprocess.call(['git', 'clone',  self.url(), self.clone_dir()], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) != 0:
            raise RuntimeError("Clone failed")

    def run(self):
        self._clone()


class BuildTask:

    def __init__(self, root, url, owner, repository, commit, threaded=True):
        self.config = IntexrationConfig.instance()
        self.url = url
        self.owner = owner
        self.repository = repository
        self.commit = commit
        self.threaded = threaded
        self.input_dir = create_dir(os.path.join(root, self.config.dir_name('temp')))
        self.output_dir = create_dir(os.path.join(root, self.config.dir_name('output'), self.owner, self.repository))

    def name(self):
        return self.owner+'/'+self.repository

    def run(self):
        logging.info("Build started for %s", self.name())
        clone_task = CloneTask(self.input_dir, self.url, self.owner, self.repository, self.commit)
        try:
            clone_task.run()
            IntexrationTask(clone_task.clone_dir(), self.output_dir, self.threaded).run()
        except RuntimeError as e:
            logging.error(e)
        finally:
            remove(clone_task.clone_dir())
        logging.info("Build finished for %s", self.name())

@Singleton
class BuildManager:

    separator = '/'

    def __init__(self):
        self.queue = {}

    @staticmethod
    def run(build, blocking=False):
        if not blocking:
            thread = Thread(target=build.run)
            thread.start()
        else:
            build.run()

    def enqueue(self, build):
        key = build.owner+self.separator+build.repository
        self.queue[key] = build

    def dequeue(self, owner, repository):
        key = owner+self.separator+repository
        self.run(self.queue[key], blocking=True)
        del self.queue[key]