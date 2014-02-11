from intexration.parser import RunArgumentParser
from intexration.server import Server, RequestHandler
from intexration.manager import ApiManager, DocumentManager, ConfigManager


class IntexrationApplication:

    def __init__(self, arguments):
        self.config_manager = ConfigManager()
        self.api_manager = ApiManager()
        self.parser = RunArgumentParser(arguments, self.config_manager, self.api_manager)
        self.build_manager = DocumentManager(threaded=self.config_manager.read_bool('COMPILATION', 'threaded'),
                                             lazy=self.config_manager.read_bool('COMPILATION', 'lazy'),
                                             explore=self.config_manager.read_bool('DOCUMENTS', 'explore'))
        self.request_handler = RequestHandler(base_url=self.config_manager.base_url(),
                                              branch=self.config_manager.read('COMPILATION', 'branch'),
                                              build_manager=self.build_manager,
                                              api_manager=self.api_manager)
        self.server = Server(host=self.config_manager.read('SERVER', 'host'),
                             port=self.config_manager.read('SERVER', 'port'),
                             handler=self.request_handler)

    def run(self):
        self.parser.parse()
        self.server.start()