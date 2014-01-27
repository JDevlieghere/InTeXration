import html
import logging
import os
import json
from bottle import Bottle, request, abort, static_file, template
from intexration.task import BuildTask, BuildManager
from intexration.intexration import IntexrationConfig
from intexration.document import Document
from intexration.api import ApiManager


class Server:

    def __init__(self, host, port, branch, lazy, threaded):
        self._host = host
        self._port = port
        self._branch = branch
        self._lazy = lazy
        self._threaded = threaded
        self._app = Bottle()
        self._route()
        self.config = IntexrationConfig.instance()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/hook/<api_key>', method="POST", callback=self._hook)
        self._app.route('/pdf/<owner>/<repository>/<name>', method=["GET", "GET"], callback=self._out)
        self._app.route('/log/<owner>/<repository>/<name>', method=["GET", "GET"], callback=self._log)
        self._app.route('/<name:path>', method="GET", callback=self._static)

    def start(self):
        self._app.run(host=self._host, port=self._port, server='cherrypy')

    def _hook(self, api_key):
        api_helper = ApiManager(self.config.file_path('api'))
        if not api_helper.is_valid(api_key):
            logging.warning("Request Denied: API key invalid")
            abort(401, 'Unauthorized: API key invalid.')
        payload = request.forms.get('payload')
        try:
            data = json.loads(payload)
            if self._branch in data['ref']:
                url = data['repository']['url']
                owner = data['repository']['owner']['name']
                repository = data['repository']['name']
                commit = data['after']
                build = BuildTask(self.config.root, url, owner, repository, commit, self._threaded)
                manager = BuildManager.instance()
                if not self._lazy:
                    manager.run(build)
                else:
                    manager.enqueue(build)
                return "InTeXration task started."
            else:
                return ""
        except ValueError:
            logging.warning("Request Denied: Could not decode request body")
            abort(400, 'Bad request: Could not decode request body.')

    def _out(self, owner, repository, name):
        global document
        try:
            document = Document(name, self.output_dir(owner, repository))
        except (RuntimeError, RuntimeWarning):
            try:
                BuildManager.instance().dequeue(owner, repository)
                document = Document(name, self.output_dir(owner, repository))
            except (RuntimeError, RuntimeWarning, KeyError):
                abort(404, "The requested document does not exist.")
        return static_file(document.pdf_name(), document.root)

    def _log(self, owner, repository, name):
        global document
        try:
            document = Document(name, self.output_dir(owner, repository))
        except (RuntimeError, RuntimeWarning):
            try:
                BuildManager.instance().dequeue(owner, repository)
                document = Document(name, self.output_dir(owner, repository))
            except (RuntimeError, RuntimeWarning, KeyError):
                abort(404, "The requested document does not exist.")
        return template(os.path.join(self.config.dir_path('templates'), 'log.tpl'),
                        root=self.config.server_root(),
                        repo=repository,
                        name=name,
                        errors=html.escape(document.get_errors()),
                        warnings=html.escape(document.get_warnings()),
                        all=html.escape(document.get_log()))

    def output_dir(self, owner, repo):
        return os.path.join(self.config.root, self.config.dir_name('output'), owner, repo)

    def _index(self):
        return template(os.path.join(self.config.dir_path('templates'), 'index.tpl'),
                        root=self.config.server_root())

    def _static(self, name):
        return static_file(name, self.config.dir_path('static'))