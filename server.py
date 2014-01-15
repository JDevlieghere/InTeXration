import json
import os
from bottle import Bottle, request, abort
import argparse


class TeXServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self._index)
        self._app.route('/hook/<api_key>', method="POST", callback=self._hook)

    def start(self):
        self._app.run(host=self._host, port=self._port)

    @staticmethod
    def validate(api_key):
        path = "api_keys.txt"
        if not os.path.isfile(path):
            return False
        key_file = open(path, "r")
        for line in key_file.readlines():
            key = line.rstrip()
            if api_key == key:
                return True
        return False

    @staticmethod
    def _index():
        return 'Welcome'

    def _hook(self,api_key):
        if not self.validate(api_key):
            abort(401, 'Unauthorized: API key invalid.')
        payload = request.forms.get('payload')
        try:
            print(payload)
            data = json.loads(payload)
            return data
        except ValueError:
            abort(400, 'Bad request: Could not decode request body.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='hostname', default='localhost')
    parser.add_argument('-port', help='port', default=8000)
    args = parser.parse_args()
    server = TeXServer(host=args.host, port=args.port)
    server.start()