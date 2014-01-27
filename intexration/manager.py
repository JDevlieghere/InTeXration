import csv
import logging
import os
import shutil
from intexration.singleton import Singleton


class ApiManager:

    NEWLINE = ''
    DELIMITER = ','

    def __init__(self, path):
        self._path = path

    def is_valid(self, key_to_check):
        with open(self._path, newline=self.NEWLINE) as key_file:
            key_reader = csv.reader(key_file, delimiter=self.DELIMITER)
            for row in key_reader:
                if key_to_check in row:
                    return True
        return False

    def add_key(self, api_key):
        with open(self._path, 'a', self.NEWLINE) as key_file:
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


class BuildManager:

    SEPARATOR = '/'

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
        key = build.owner+self.SEPARATOR+build.repository
        self.queue[key] = build

    def dequeue(self, key):
        return self.queue[key]
        del self.queue[key]

    def run_lazy(self, owner, repository):
        key = owner+self.SEPARATOR+repository
        if key in self.queue:
            build = self.dequeue(key)
            self.run(build, blocking=True)