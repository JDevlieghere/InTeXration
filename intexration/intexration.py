import logging
import os
import logging.config
import sys
from intexration.server import Server, RequestHandler
from intexration import constants
from intexration.manager import ApiManager, DocumentManager, ConfigManager


class Intexration:

    def __init__(self, arguments):
        logging.config.fileConfig(os.path.join(constants.PATH_ROOT,
                                               constants.DIRECTORY_CONFIG,
                                               constants.FILE_LOGGER))
        self.config = ConfigManager()
        self.parser = IntexrationParser(self.config, arguments)
        self.build_manager = DocumentManager(threaded=self.config.read_bool('COMPILATION', 'threaded'),
                                             lazy=self.config.read_bool('COMPILATION', 'lazy'),
                                             explore=self.config.read_bool('INTEXRATION', 'explore'),
                                             output=self.config.read('INTEXRATION', 'output'))
        self.api_manager = ApiManager()
        self.request_handler = RequestHandler(base_url=self.config.base_url(),
                                              branch=self.config.read('COMPILATION', 'branch'),
                                              build_manager=self.build_manager,
                                              api_manager=self.api_manager)
        self.server = Server(host=self.config.read('SERVER', 'host'),
                             port=self.config.read('SERVER', 'port'),
                             handler=self.request_handler)

    def run(self):
        self.parser.parse()
        self.server.start()


class IntexrationParser:

    def __init__(self, arguments, config):
        self.arguments = arguments
        self.config = config
        self.exit = False

    def get(self, argument):
        return getattr(self.arguments, argument)

    def is_set(self, argument):
        return hasattr(self.arguments, argument) and getattr(self.arguments, argument) is not None

    def is_true(self, argument):
        return hasattr(self.arguments, argument) and hasattr(self.arguments, argument)

    def parse(self):
        self._parse_config()
        self._parse_api()
        self._exit()

    def _parse_config(self):
        if self.is_set('config_host'):
            self.config.write('SERVER', 'host', self.get('config_host'))
            self._exit_on_finish()
        if self.is_set('config_port'):
            self.config.write('SERVER', 'port', self.get('config_port'))
            self._exit_on_finish()
        if self.is_set('config_export'):
            self.config.file_export(self.get('config_export'))
            self._exit_on_finish()
        if self.is_set('config_import'):
            self.config.file_import(self.get('config_import'))
            self._exit_on_finish()

    def _parse_api(self):
        api_manager = ApiManager()
        if self.is_set('api_add'):
            api_manager.add_key(self.get('api_add'))
            self._exit_on_finish()
        if self.is_set('api_remove'):
            api_manager.remove_key(self.get('api_remove'))
            self._exit_on_finish()
        if self.is_true('api_list'):
            for line in api_manager.all_keys():
                print(line[0])
            self._exit_on_finish()
        if self.is_set('api_export'):
            api_manager.export_file(self.get('api_export'))
            self._exit_on_finish()
        if self.is_set('api_import'):
            api_manager.import_file(self.get('api_import'))
            self._exit_on_finish()

    def _exit_on_finish(self):
        self.exit = True

    def _exit(self):
        if self.exit:
            sys.exit(0)
