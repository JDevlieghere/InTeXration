import logging
from bottle import Bottle, request, abort, static_file, template
import os
import json
from build.lib.intexration import build
from intexration import config
from intexration.build import Build, CloneBuild, LazyBuild
from intexration.document import Document
from intexration.helper import ApiHelper


class Server:

    output_name = 'out'

    def __init__(self, host, port, branch, lazy):
        self._host = host
        self._port = port
        self._branch = branch
        self._lazy = lazy
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/hook/<api_key>', method="POST", callback=self._hook)
        self._app.route('/pdf/<owner>/<repository>/<name>', method=["GET", "GET"], callback=self._out)
        self._app.route('/log/<owner>/<repository>/<name>', method=["GET", "GET"], callback=self._log)
        self._app.route('/<name:path>', method="GET", callback=self._static)

    def start(self):
        self._app.run(host=self._host, port=self._port, server='cherrypy')

    def _hook(self, api_key):
        api_helper = ApiHelper(config.FILE_API_KEY)
        if not api_helper.is_valid(api_key):
            logging.warning("Request Denied: API key invalid")
            abort(401, 'Unauthorized: API key invalid.')
        payload = request.forms.get('payload')
        try:
            data = json.loads(payload)
            if self._branch in data['ref']:
                owner = data['repository']['owner']['name']
                repository = data['repository']['name']
                commit = data['after']
                if not self._lazy:
                    Build(config.PATH_ROOT, owner, repository, commit).run()
                else:
                    build.empty(os.path.join(self.output_dir(owner, repository)))
                return "InTeXration task started."
            else:
                return ""
        except ValueError:
            logging.warning("Request Denied: Could not decode request body")
            abort(400, 'Bad request: Could not decode request body.')

    def _out(self, owner, repository, name):
        try:
            document = Document(name, self.output_dir(owner, repository))
        except (RuntimeError, RuntimeWarning):
            try:
                Build(config.PATH_ROOT, owner, repository, name).run()
                document = Document(name, self.output_dir(owner, repository))
            except (RuntimeError, RuntimeWarning):
                abort(404, "The requested document does not exist.")
        return static_file(document.pdf_name(), document.root)

    def _log(self, owner, repository, name):
        try:
            document = Document(name, self.output_dir(owner, repository))
        except (RuntimeError, RuntimeWarning):
            try:
                Build(config.PATH_ROOT, owner, repository, name).run()
                document = Document(name, self.output_dir(owner, repository))
            except (RuntimeError, RuntimeWarning):
                abort(404, "The requested document does not exist.")
        return template(os.path.join(config.PATH_TEMPLATES, 'log.tpl'),
                        root=config.SERVER_ROOT, repo=repository, name=name, errors=document.get_errors(),
                        warnings=document.get_warnings(), all=document.get_log())

    def output_dir(self, owner, repo):
        return os.path.join(config.PATH_ROOT, self.output_name, owner, repo)

    @staticmethod
    def _index():
        return template(os.path.join(config.PATH_TEMPLATES, 'index.tpl'), root=config.SERVER_ROOT)
        #return template(os.path.join(config.PATH_TEMPLATES, 'list.tpl'), root=config.SERVER_ROOT,
        #                documents=DocumentExplorer(config.PATH_OUTPUT).all_documents())

    @staticmethod
    def _static(name):
        return static_file(name, config.PATH_STATIC)