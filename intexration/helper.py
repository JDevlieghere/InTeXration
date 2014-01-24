import csv
import logging
import os
import shutil
from intexration.intexration import IntexrationConfig


class ApiHelper:
    def __init__(self, path):
        self._path = path
        self.config = IntexrationConfig.Instance()

    def is_valid(self, key_to_check):
        with open(self._path, newline='') as key_file:
            key_reader = csv.reader(key_file, delimiter=',')
            for row in key_reader:
                if key_to_check in row:
                    return True
        return False

    def add(self, api_key):
        with open(self._path, 'a', newline='') as key_file:
            key_writer = csv.writer(key_file, delimiter=',', quoting=csv.QUOTE_NONE)
            key_writer.writerow([api_key])

    def get_all(self):
        key_file = open(self._path, 'r', newline='')
        rows = list(csv.reader(key_file, delimiter=','))
        key_file.close()
        return rows

    def remove(self, api_key):
        rows = []
        for row in self.get_all():
            if api_key not in row:
                rows.append(row)
        with open(self._path, 'w', newline='') as key_file:
            key_writer = csv.writer(key_file, delimiter=',')
            for row in rows:
                key_writer.writerow(row)

    def export_file(self, dir):
        path = os.path.join(dir, self.file_names['api'])
        shutil.copyfile(self._path, path)
        logging.info("API key file exported to %s", path)

    def import_file(self, dir):
        path = os.path.join(dir, self.file_names['api'])
        if not os.path.exists(path):
            logging.error("Importing API key file failed: %s not found.", self.file_names['api'])
            return
        shutil.copyfile(path, self._path)
        logging.info("API key file imported from %s", path)
