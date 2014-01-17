import logging
from bottle import Bottle, request, abort, static_file, template
import os
import json
from intexration.helper import LogHelper
from intexration.task import Task


class Server:
    def __init__(self, host, port, api_keys):
        self._host = host
        self._port = port
        self._base_url = 'http://' + host + ':' + port
        self._api_keys = api_keys
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/hook/<api_key>', method="POST", callback=self._hook)
        self._app.route('/out/<repo>/<name>', method=["GET", "GET"], callback=self._out)
        self._app.route('/log/<repo>/<name>', method=["GET", "GET"], callback=self._log)
        self._app.route('/css/<name>', method="GET", callback=self._css)

    def start(self):
        self._app.run(host=self._host, port=self._port)

    def _hook(self, api_key):
        def validate(key_to_check):
            path = self._api_keys
            if not os.path.isfile(path):
                return False
            key_file = open(path, "r")
            for line in key_file.readlines():
                key = line.rstrip()
                if key_to_check == key:
                    return True
            return False

        if not validate(api_key):
            logging.warning("Request Denied: API key invalid.")
            abort(401, 'Unauthorized: API key invalid.')
        payload = request.forms.get('payload')
        try:
            data = json.loads(payload)
            url = data['repository']['url']
            name = data['repository']['name']
            commit = data['after']
            task = Task(url, name, commit)
            task.run()
            return 'InTeXration task started.'
        except ValueError:
            logging.warning("Request Denied: Could not decode request body.")
            abort(400, 'Bad request: Could not decode request body.')

    def _index(self):
        return template('templates/index', base_url=self._baseurl)

    @staticmethod
    def _css(name):
        file_name = name + '.css'
        path = os.path.join(os.getcwd(), 'templates')
        return static_file(file_name, path)

    @staticmethod
    def _out(repo, name):
        path = os.path.join(os.getcwd(), 'out', repo)
        file_name = name + '.pdf'
        return static_file(file_name, path)

    def _log(self, repo, name):
        file_name = name + '.log'
        path = os.path.join(os.getcwd(), 'out', repo, file_name)
        log_handler = LogHelper(path)
        return template('templates/log', repo=repo, name=name, errors=log_handler.get_errors(),
                        warnings=log_handler.get_warnings(), all=log_handler.get_all(), base_url=self._baseurl)
