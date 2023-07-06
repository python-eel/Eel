import os
import socket
import http.server
import sys
import threading
from http.server import HTTPServer

from resource_path import resource_path

class MyServer:
    def __init__(self):
        self.server_thread = None
        self.httpd = None

    def is_port_in_use(self, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', PORT)) == 0

    def start_server(self, PATH, PORT):
        web_dir = resource_path(PATH)
        os.chdir(web_dir)
        Handler = http.server.SimpleHTTPRequestHandler

        self.httpd = HTTPServer(("", PORT), Handler)
        print(f"Starting server at port {PORT} from {web_dir}")
        try:
            self.httpd.serve_forever()
            print(f"Server started successfully at port {PORT}")
        except Exception as e:
            print(f"Failed to start server at port {PORT}. Error: {e}")

    def stop_server(self):
        if self.httpd is not None:
            try:
                self.httpd.server_close()
            except Exception as e:
                print(f"Failed to stop server. Error: {e}")

    def start(self, PATH, PORT):
        self.server_thread = threading.Thread(target=self.start_server, args=(PATH, PORT,))
        self.server_thread.start()

    def stop(self):
        stop_server_thread = threading.Thread(target=self.stop_server)
        stop_server_thread.start()
        stop_server_thread.join()
        if self.server_thread is not None:
            self.server_thread.join()