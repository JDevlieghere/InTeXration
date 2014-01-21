import logging
from bottle import Bottle, request, abort, static_file, template
import os
import json
from intexration import config
from intexration.build import Build
from intexration.document import Document
from intexration.helper import ApiHelper


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/hook/<api_key>', method="POST", callback=self._hook)
        self._app.route('/pdf/<owner>/<repo>/<name>', method=["GET", "GET"], callback=self._out)
        self._app.route('/log/<owner>/<repo>/<name>', method=["GET", "GET"], callback=self._log)
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
            owner = data['repository']['owner']['name']
            repository = data['repository']['name']
            commit = data['after']
            Build(config.PATH_ROOT, owner, repository, commit).run()
            return 'InTeXration task started.'
        except ValueError:
            logging.warning("Request Denied: Could not decode request body")
            abort(400, 'Bad request: Could not decode request body.')

    @staticmethod
    def _index():
        return template(os.path.join(config.PATH_TEMPLATES, 'index'), root=config.SERVER_ROOT)
        #return template(os.path.join(config.PATH_TEMPLATES, 'list.tpl'), root=config.SERVER_ROOT,
        #                documents=DocumentExplorer(config.PATH_OUTPUT).all_documents())

    @staticmethod
    def _static(name):
        return static_file(name, config.PATH_STATIC)

    @staticmethod
    def _out(owner, repo, name):
        document = Document(name, Server.root(owner, repo))
        return static_file(document.pdf_name(), document.root)

    @staticmethod
    def _log(owner, repo, name):
        logging.debug(Server.root(owner, repo))
        document = Document(name, Server.root(owner, repo))
        return template(os.path.join(config.PATH_TEMPLATES, 'log'), root=config.SERVER_ROOT, repo=repo, name=name,
                        errors=document.get_errors(), warnings=document.get_warnings(), all=document.get_log())

    @staticmethod
    def root(owner, repo):
        return os.path.join(config.PATH_OUTPUT, owner, repo)