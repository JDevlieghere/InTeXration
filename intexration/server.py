import logging
import os
import json
from bottle import Bottle, request, abort, static_file, template
from intexration.task import BuildTask
from intexration.document import Document


class Server:

    SERVER = 'cherrypy'

    def __init__(self, host, port, handler):
        self._host = host
        self._port = port
        self._handler = handler
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._handler.index_request)
        self._app.route('/hook/<api_key>', method="POST", callback=self._handler.hook_request)
        self._app.route('/pdf/<owner>/<repository>/<name>', method=["GET", "GET"], callback=self._handler.pdf_request)
        self._app.route('/log/<owner>/<repository>/<name>', method=["GET", "GET"], callback=self._handler.log_request)
        self._app.route('/<name:path>', method="GET", callback=self._handler.file_request)

    def start(self):
        self._app.run(host=self._host,
                      port=self._port,
                      server=self.SERVER)


class RequestHandler:

    DIRECTORY_STATIC = 'static'
    DIRECTORY_OUTPUT = 'out'
    TEMPLATE_INDEX = 'index'
    TEMPLATE_LOG = 'log'

    def __init__(self, root, base_url, branch, threaded, lazy, build_manager, api_manager):
        self._root = root
        self._base_url = base_url
        self._branch = branch
        self._threaded = threaded
        self._lazy = lazy
        self.build_manager = build_manager
        self.api_manager = api_manager

    def to_dir(self, owner, repo):
        return os.path.join(self._root, self.DIRECTORY_OUTPUT, owner, repo)

    def index_request(self):
        return template(self.TEMPLATE_INDEX,
                        base_url=self._base_url)

    def hook_request(self, api_key):
        if not self.api_manager.is_valid(api_key):
            self.abort_request(401, 'Unauthorized: API key invalid.')
        try:
            data = json.loads(request.forms.get('payload'))
            refs = data['ref']
            url = data['repository']['url']
            owner = data['repository']['owner']['name']
            repository = data['repository']['name']
            commit = data['after']
            if self._branch in refs:
                build = BuildTask(self._root, url, owner, repository, commit, self._threaded)
                if not self._lazy:
                    self.build_manager.run(build)
                else:
                    self.build_manager.enqueue(build)
            else:
                self.abort_request(406, "Wrong branch")
        except (RuntimeError, RuntimeWarning) as e:
            self.abort_request(500, e)

    def pdf_request(self, owner, repository, name):
        self.build_manager.run_lazy(owner, repository)
        try:
            document = Document(name, self.to_dir(owner, repository))
            return static_file(document.pdf_name(), document.root)
        except (RuntimeError, RuntimeWarning):
            self.abort_request(404, "The requested document does not exist.")

    def log_request(self, owner, repository, name):
        self.build_manager.run_lazy(owner, repository)
        try:
            document = Document(name, self.to_dir(owner, repository))
            return template(self.TEMPLATE_LOG,
                            base_url=self._base_url,
                            repo=repository,
                            name=name,
                            errors=document.get_errors(),
                            warnings=document.get_warnings(),
                            all=document.get_log())
        except (RuntimeError, RuntimeWarning):
            self.abort_request(404, "The requested document does not exist.")

    def file_request(self, name):
        static_dir = os.path.join(self._root, self.DIRECTORY_STATIC)
        return static_file(name, static_dir)

    @staticmethod
    def abort_request(code, text):
        logging.warning(text)
        abort(code, text)
