import logging
import os
import logging.config

from intexration.parser import RunArgumentParser
from intexration.server import Server, RequestHandler
from intexration import constants
from intexration.manager import ApiManager, DocumentManager, ConfigManager


class IntexrationApplication:

    def __init__(self, arguments):
        logging.config.fileConfig(os.path.join(constants.PATH_ROOT,
                                               constants.DIRECTORY_CONFIG,
                                               constants.FILE_LOGGER))
        self.config = ConfigManager()
        self.parser = RunArgumentParser(arguments, self.config)
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