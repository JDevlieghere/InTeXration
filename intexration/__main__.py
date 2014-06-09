from intexration.server import Server, RequestHandler
from intexration.manager import ApiManager, DocumentManager, ConfigManager, LoggingManager


class InTeXration:

    def __init__(self):
        self.logging_manager = LoggingManager()
        self.config_manager = ConfigManager()
        self.api_manager = ApiManager()
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
        self.server.start()


def version():
    return '1.3.0 dev'


def main():
    InTeXration().run()


if __name__ == '__main__':
    main()