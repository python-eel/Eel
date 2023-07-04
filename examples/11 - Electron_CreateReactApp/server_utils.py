import os
import socket
import http.server
import socketserver
from resource_path import resource_path


def is_port_in_use(PORT):
    # If the code is 0, it means the connection was successful, indicating that the port is in use. 
    # If the code is any other value, it means the connection attempt failed, indicating that the port is available.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', PORT)) == 0
    
def start_server(PATH, PORT):
    # Start the local server to serve the React app
    web_dir = resource_path(PATH)  # exact path you need
    os.chdir(web_dir)  # change the current working directory

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"serving at port {PORT} from {web_dir}")
        httpd.serve_forever()