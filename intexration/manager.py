import configparser
import csv
import logging
import os
import shutil
from threading import Thread
from intexration.document import Document
from intexration import constants
from intexration.build import Identifier
from intexration.task import CompileTask, CloneTask


class LoggingManager:

    DEFAULT_LOGGER = 'logger.default.cfg'

    def __init__(self):
        self.path = os.path.join(constants.PATH_USER,
                                 constants.DIRECTORY_CONFIG,
                                 constants.FILE_LOGGER)
        if not os.path.exists(self.path):
            self._copy_default()
        logging.config.fileConfig(self.path)

    def _copy_default(self):
        source_path = os.path.join(constants.PATH_ROOT,
                                   constants.DIRECTORY_CONFIG,
                                   self.DEFAULT_LOGGER)
        shutil.copyfile(source_path, self.path)


class ConfigManager:

    DEFAULT_CONFIG = 'config.default.cfg'

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.path = os.path.join(constants.PATH_USER,
                                 constants.DIRECTORY_CONFIG,
                                 constants.FILE_CONFIG)
        self.validate()

    def validate(self):
        if not os.path.exists(self.path):
            self._copy_default()
        if not os.path.exists(self.logger_file):
            raise RuntimeError("Logger config file missing")
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

    @staticmethod
    def file_export(directory):
        path = os.path.join(directory, constants.FILE_CONFIG)
        shutil.copyfile(os.path.join(constants.PATH_MODULE, constants.DIRECTORY_CONFIG, constants.FILE_CONFIG), path)
        logging.info("Configuration exported to %s", path)

    def file_import(self, directory, name=constants.FILE_CONFIG):
        path = os.path.join(directory, name)
        if not os.path.exists(path):
            raise RuntimeError("Importing configuration failed: not found in %s".format(path))
        shutil.copyfile(path, os.path.join(constants.PATH_MODULE, constants.DIRECTORY_CONFIG, constants.FILE_CONFIG))
        self.validate()
        logging.info("Configuration imported from %s", path)

    def base_url(self):
        return 'http://'+self.read('SERVER', 'host')+':'+self.read('SERVER', 'port')+'/'

    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    def _copy_default(self):
        source_path = os.path.join(constants.PATH_MODULE, constants.DIRECTORY_CONFIG, self.DEFAULT_CONFIG)
        self.file_import(source_path, self.path)


class ApiManager:

    NEWLINE = ''
    DELIMITER = ','

    def __init__(self):
        self._path = os.path.join(constants.PATH_USER,
                                  constants.DIRECTORY_DATA,
                                  constants.FILE_API)
        if not os.path.exists(self._path):
            self.create_default_file()

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

    def export_file(self, directory):
        path = os.path.join(directory, os.path.basename(self._path))
        shutil.copyfile(self._path, path)
        logging.info("API key file exported to %s", path)

    def import_file(self, directory):
        path = os.path.join(directory, os.path.basename(self._path))
        if not os.path.exists(path):
            logging.error("Importing API key file failed: file not found.")
            return
        shutil.copyfile(path, self._path)
        logging.info("API key file imported from %s", path)

    def create_default_file(self):
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