import logging
from bottle import Bottle, request, abort, static_file, template
import os
import json
from intexration import config
from intexration.helper import LogHelper, ApiHelper
from intexration.task import Task


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/hook/<api_key>', method="POST", callback=self._hook)
        self._app.route('/out/<owner>/<repo>/<name>', method=["GET", "GET"], callback=self._out)
        self._app.route('/log/<owner>/<repo>/<name>', method=["GET", "GET"], callback=self._log)
        self._app.route('/<name:path>', method="GET", callback=self._static)

    def start(self):
        self._app.run(host=self._host, port=self._port, server='cherrypy')

    def _hook(self, api_key):
        api_helper = ApiHelper(config.FILE_API_KEY)
        if not api_helper.is_valid(api_key):
            logging.warning("Request Denied: API key invalid.")
            abort(401, 'Unauthorized: API key invalid.')
        payload = request.forms.get('payload')
        try:
            data = json.loads(payload)
            url = data['repository']['url']
            name = data['repository']['name']
            owner = data['repository']['owner']['name']
            commit = data['after']
            task = Task(url, name, owner, commit)
            task.run()
            return 'InTeXration task started.'
        except ValueError:
            logging.warning("Request Denied: Could not decode request body.")
            abort(400, 'Bad request: Could not decode request body.')

    @staticmethod
    def _index():
        return template(os.path.join(config.PATH_TEMPLATES, 'index.tpl'), root=config.SERVER_ROOT)

    @staticmethod
    def _static(name):
        return static_file(name, config.PATH_STATIC)

    @staticmethod
    def _out(owner, repo, name):
        path = os.path.join(config.PATH_OUTPUT, owner, repo)
        file_name = name + '.pdf'
        return static_file(file_name, path)

    @staticmethod
    def _log(owner, repo, name):
        file_name = name + '.log'
        path = os.path.join(config.PATH_OUTPUT, owner, repo, file_name)
        log_handler = LogHelper(path)
        return template(os.path.join(config.PATH_TEMPLATES, 'log.tpl'), root=config.SERVER_ROOT, repo=repo, name=name,
                        errors=log_handler.get_errors(), warnings=log_handler.get_warnings(), all=log_handler.get_all())
