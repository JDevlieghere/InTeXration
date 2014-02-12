import configparser
import csv
import logging.config
import os
import shutil
from threading import Thread
from intexration.tools import create_dir
from intexration.document import Document
from intexration import constants
from intexration.build import Identifier
from intexration.task import CompileTask, CloneTask


class LoggingManager:

    DEFAULT_LOGGER = 'logging.default.cfg'
    LOG_DIR = 'log'

    def __init__(self):
        self._root = os.path.join(constants.PATH_USER,
                                  constants.DIRECTORY_CONFIG)
        self.path = os.path.join(self._root,
                                 constants.FILE_LOGGER)
        self._create_missing_output()
        self._copy_missing_default()
        logging.config.fileConfig(self.path)

    def _copy_missing_default(self):
        if not os.path.exists(self.path):
            create_dir(self._root)
            source_path = os.path.join(constants.PATH_MODULE,
                                       constants.DIRECTORY_CONFIG,
                                       self.DEFAULT_LOGGER)
            shutil.copyfile(source_path, self.path)

    def _create_missing_output(self):
        output_path = os.path.join(constants.PATH_USER,
                                   self.LOG_DIR)
        if not os.path.exists(output_path):
            create_dir(output_path)


class ConfigManager:

    DEFAULT_CONFIG = 'config.default.cfg'

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self._root = os.path.join(constants.PATH_USER,
                                  constants.DIRECTORY_CONFIG)
        self.path = os.path.join(self._root,
                                 constants.FILE_CONFIG)
        self.validate()

    def validate(self):
        self._copy_missing_default()
        try:
            self.read('SERVER', 'host')
            self.read('SERVER', 'port')
            self.read('COMPILATION', 'branch')
            self.read('COMPILATION', 'lazy')
            self.read('COMPILATION', 'threaded')
        except configparser.Error:
            raise RuntimeError("Invalid config file")

    def read(self, section, key):
        self.parser.read(self.path)
        return self.parser[section][key]

    def read_bool(self, section, key):
        return self.str2bool(self.read(section, key))

    def write(self, section, key, value):
        self.parser.read(self.path)
        self.parser.set(section, key, value)
        with open(self.path, 'w+') as configfile:
            self.parser.write(configfile)
        logging.info("Updated config value (%s)", value)

    def base_url(self):
        return 'http://'+self.read('SERVER', 'host')+':'+self.read('SERVER', 'port')+'/'

    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    def _copy_missing_default(self):
        if not os.path.exists(self.path):
            create_dir(self._root)
            source_path = os.path.join(constants.PATH_MODULE, constants.DIRECTORY_CONFIG, self.DEFAULT_CONFIG)
            shutil.copyfile(source_path, self.path)


class ApiManager:

    NEWLINE = ''
    DELIMITER = ','

    def __init__(self):
        self._root = os.path.join(constants.PATH_USER,
                                  constants.DIRECTORY_DATA)
        self._path = os.path.join(self._root,
                                  constants.FILE_API)
        self._create_missing_default()

    def is_valid(self, key_to_check):
        with open(self._path, newline=self.NEWLINE) as key_file:
            key_reader = csv.reader(key_file, delimiter=self.DELIMITER)
            for row in key_reader:
                if key_to_check in row:
                    return True
        return False

    def add_key(self, api_key):
        with open(self._path, 'a', newline=self.NEWLINE) as key_file:
            key_writer = csv.writer(key_file, delimiter=self.DELIMITER, quoting=csv.QUOTE_NONE)
            key_writer.writerow([api_key])

    def all_keys(self):
        key_file = open(self._path, 'r', newline=self.NEWLINE)
        rows = list(csv.reader(key_file, delimiter=self.DELIMITER))
        key_file.close()
        return rows

    def remove_key(self, api_key):
        rows = []
        for row in self.all_keys():
            if api_key not in row:
                rows.append(row)
        with open(self._path, 'w', newline=self.NEWLINE) as key_file:
            key_writer = csv.writer(key_file, delimiter=self.DELIMITER)
            for row in rows:
                key_writer.writerow(row)

    def _create_missing_default(self):
        if not os.path.exists(self._path):
            create_dir(self._root)
            file = open(self._path, 'w+')
            file.close()
            logging.info("No api key file found, empty file created.")


class DocumentManager:

    def __init__(self, threaded, lazy, explore):
        self.threaded = threaded
        self.lazy = lazy
        self.build_queue = dict()
        self.documents = dict()
        self.output = os.path.join(constants.PATH_USER,
                                   constants.DIRECTORY_OUTPUT)
        create_dir(self.output)
        if explore:
            self.explore_documents()

    def explore_documents(self):
        root = self.output
        for owner in os.listdir(root):
            for repository in os.listdir(os.path.join(root, owner)):
                for file in os.listdir(os.path.join(root, owner, repository)):
                    path = os.path.join(root, owner, repository)
                    name = os.path.splitext(file)[0]
                    identifier = Identifier(owner, repository, name)
                    try:
                        document = Document(name, path)
                        self.submit_document(identifier, document)
                        logging.info("Document %s found on disk", identifier)
                    except RuntimeError:
                        pass

    def submit_request(self, request):
        CloneTask(self, request).run()

    def submit_builds(self, builds):
        if not self.lazy:
            self._build_all(builds)
        else:
            for identifier in builds:
                self.enqueue(identifier, builds[identifier])

    def submit_document(self, identifier, document):
        self.documents[identifier] = document

    def enqueue(self, identifier, build):
        if identifier in self.build_queue:
            previous_build = self.build_queue[identifier]
            previous_build.finish()
        self.build_queue[identifier] = build
        logging.info("Queued %s", identifier)

    def is_queued(self, identifier):
        return identifier in self.build_queue

    def is_ready(self, identifier):
        return identifier not in self.build_queue and identifier in self.documents

    def _build_from_queue(self, identifier):
        build = self.build_queue[identifier]
        task = CompileTask(self, identifier, build)
        task.run()

    def _build_all(self, builds):
        threads = []
        for identifier in builds:
            build = builds[identifier]
            task = CompileTask(self, identifier, build)
            if self.threaded:
                threads.append(Thread(target=task.run))
            else:
                task.run()
        [t.start() for t in threads]
        [t.join() for t in threads]

    def get_document(self, identifier):
        if self.is_ready(identifier):
            return self.documents.get(identifier)
        if self.is_queued(identifier):
            self._build_from_queue(identifier)
            return self.documents.get(identifier)
        raise RuntimeWarning("No document found for %s".format(identifier))

    def get_documents(self):
        return dict(self.documents)

    def get_queue(self):
        return dict(self.build_queue)