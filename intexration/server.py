import logging
import os
import json
from bottle import Bottle, request, abort, static_file, template
import bottle
from intexration import constants
from intexration.build import BuildRequest, Identifier


class Server:

    SERVER = 'cherrypy'

    def __init__(self, host, port, handler):
        bottle.TEMPLATE_PATH.insert(0, os.path.join(constants.PATH_MODULE, constants.DIRECTORY_TEMPLATES))
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

    TEMPLATE_INDEX = 'index'
    TEMPLATE_LOG = 'log'

    def __init__(self, base_url, branch, build_manager, api_manager):
        self._base_url = base_url
        self._branch = branch
        self.build_manager = build_manager
        self.api_manager = api_manager

    def index_request(self):
        return template(self.TEMPLATE_INDEX,
                        base_url=self._base_url,
                        documents=self.build_manager.get_documents(),
                        queue=self.build_manager.get_queue(),
                        branch=self._branch,
                        lazy=self.build_manager.lazy,
                        threaded=self.build_manager.threaded)

    def hook_request(self, api_key):
        if not self.api_manager.is_valid(api_key):
            self.abort_request(401, 'Unauthorized: API key invalid.')
        try:
            data = json.loads(request.forms.get('payload'))
            refs = data['ref']
            url = data['repository']['url']
            ssh = data['repository']['ssh_url']
            owner = data['repository']['owner']['name']
            repository = data['repository']['name']
            commit = data['after']
            if self._branch in refs:
                build_request = BuildRequest(owner, repository, commit, url)
                self.build_manager.submit_request(build_request)
            else:
                self.abort_request(406, "Wrong branch")
        except (RuntimeError, RuntimeWarning) as e:
            self.abort_request(500, e)

    def pdf_request(self, owner, repository, name):
        try:
            identifier = Identifier(owner, repository, name)
            document = self.build_manager.get_document(identifier)
            return static_file(document.pdf, document.path)
        except (RuntimeError, RuntimeWarning):
            self.abort_request(404, "The requested document does not exist.")

    def log_request(self, owner, repository, name):
        try:
            identifier = Identifier(owner, repository, name)
            document = self.build_manager.get_document(identifier)
            return template(self.TEMPLATE_LOG,
                            base_url=self._base_url,
                            identifier=identifier,
                            errors=document.errors(),
                            warnings=document.warnings(),
                            all=document.logs())
        except (RuntimeError, RuntimeWarning):
            self.abort_request(404, "The requested document does not exist.")

    @staticmethod
    def file_request(name):
        static_dir = os.path.join(constants.PATH_MODULE, constants.DIRECTORY_STATIC)
        return static_file(name, static_dir)

    @staticmethod
    def abort_request(code, text):
        logging.warning(text)
        abort(code, text)
