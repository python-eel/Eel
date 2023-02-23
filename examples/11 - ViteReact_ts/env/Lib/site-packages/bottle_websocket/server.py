import logging
from bottle import ServerAdapter
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.logging import create_logger


class GeventWebSocketServer(ServerAdapter):
    def run(self, handler):
        server = pywsgi.WSGIServer((self.host, self.port), handler, handler_class=WebSocketHandler)

        if not self.quiet:
            server.logger = create_logger('geventwebsocket.logging')
            server.logger.setLevel(logging.INFO)
            server.logger.addHandler(logging.StreamHandler())

        server.serve_forever()
