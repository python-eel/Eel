from __future__ import print_function   # Python 2 compatibility stuff
from builtins import range
from io import open

import gevent as gvt
import json as jsn
import bottle as btl
import bottle.ext.websocket as wbs
import re as rgx
import os
import eel.browsers as brw
import random as rnd
import sys
import pkg_resources as pkg
import socket

_eel_js_file = pkg.resource_filename('eel', 'eel.js')
_eel_js = open(_eel_js_file, encoding='utf-8').read()
_websockets = []
_call_return_values = {}
_call_return_callbacks = {}
_call_number = 0
_exposed_functions = {}
_js_functions = []
_mock_queue = []
_mock_queue_done = set()

# All start() options must provide a default value and explanation here
_start_args = {
    'mode':             'chrome',                   # What browser is used
    'host':             'localhost',                # Hostname use for Bottle server
    'port':             8000,                       # Port used for Bottle server (use 0 for auto)
    'block':            True,                       # Whether start() blocks calling thread
    'jinja_templates':  None,                       # Folder for jinja2 templates
    'cmdline_args':     ['--disable-http-cache'],   # Extra cmdline flags to pass to browser start
    'size':             None,                       # (width, height) of main window
    'position':         None,                       # (left, top) of main window
    'geometry':         {},                         # Dictionary of size/position for all windows
    'close_callback':   None,                       # Callback for when all windows have closed
    'app_mode':  True,                              # (Chrome specific option)
    'all_interfaces': False,                        # Allow bottle server to listen for connections on all interfaces
    'disable_cache': True,                          # Sets the no-store response header when serving assets
    'app': None,                                    # Allows passing in a custom Bottle instance, e.g. with middleware
}

# == Temporary (suppressable) error message to inform users of breaking API change for v1.0.0 ===
_start_args['suppress_error'] = False
api_error_message = '''
----------------------------------------------------------------------------------
  'options' argument deprecated in v1.0.0, see https://github.com/ChrisKnott/Eel
  To suppress this error, add 'suppress_error=True' to start() call.
  This option will be removed in future versions
----------------------------------------------------------------------------------
'''
# ===============================================================================================

# Public functions

def expose(name_or_function=None):
    # Deal with '@eel.expose()' - treat as '@eel.expose'
    if name_or_function is None:
        return expose

    if type(name_or_function) == str:   # Called as '@eel.expose("my_name")'
        name = name_or_function

        def decorator(function):
            _expose(name, function)
            return function
        return decorator
    else:
        function = name_or_function
        _expose(function.__name__, function)
        return function


def init(path, allowed_extensions=['.js', '.html', '.txt', '.htm',
                                   '.xhtml', '.vue']):
    global root_path, _js_functions
    root_path = _get_real_path(path)

    js_functions = set()
    for root, _, files in os.walk(root_path):
        for name in files:
            if not any(name.endswith(ext) for ext in allowed_extensions):
                continue

            try:
                with open(os.path.join(root, name), encoding='utf-8') as file:
                    contents = file.read()
                    expose_calls = set()
                    finder = rgx.findall(r'eel\.expose\(([^\)]+)\)', contents)
                    for expose_call in finder:
                        # If name specified in 2nd argument, strip quotes and store as function name
                        if ',' in expose_call:
                            expose_call = rgx.sub(r'["\']', '', expose_call.split(',')[1])
                        expose_call = expose_call.strip()
                        # Verify that function name is valid
                        msg = "eel.expose() call contains '(' or '='"
                        assert rgx.findall(r'[\(=]', expose_call) == [], msg
                        expose_calls.add(expose_call)
                    js_functions.update(expose_calls)
            except UnicodeDecodeError:
                pass    # Malformed file probably

    _js_functions = list(js_functions)
    for js_function in _js_functions:
        _mock_js_function(js_function)


def start(*start_urls, **kwargs):
    _start_args.update(kwargs)

    if 'options' in kwargs:
        if _start_args['suppress_error']:
            _start_args.update(kwargs['options'])
        else:
            raise RuntimeError(api_error_message)

    if _start_args['port'] == 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        _start_args['port'] = sock.getsockname()[1]
        sock.close()

    if _start_args['jinja_templates'] != None:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        templates_path = os.path.join(root_path, _start_args['jinja_templates'])
        _start_args['jinja_env'] = Environment(loader=FileSystemLoader(templates_path),
                                 autoescape=select_autoescape(['html', 'xml']))


    # Launch the browser to the starting URLs
    show(*start_urls)

    def run_lambda():
        if _start_args['all_interfaces'] == True:
            HOST = '0.0.0.0'
        else:
            HOST = _start_args['host']
        return btl.run(
            host=HOST,
            port=_start_args['port'],
            server=wbs.GeventWebSocketServer,
            quiet=True,
            app=_start_args.get('app'))

    # Start the webserver
    if _start_args['block']:
        run_lambda()
    else:
        spawn(run_lambda)


def show(*start_urls):
    brw.open(start_urls, _start_args)


def sleep(seconds):
    gvt.sleep(seconds)


def spawn(function, *args, **kwargs):
    gvt.spawn(function, *args, **kwargs)

# Bottle Routes

@btl.route('/eel.js')
def _eel():
    start_geometry = {'default': {'size': _start_args['size'],
                                  'position': _start_args['position']},
                      'pages':   _start_args['geometry']}

    page = _eel_js.replace('/** _py_functions **/',
                           '_py_functions: %s,' % list(_exposed_functions.keys()))
    page = page.replace('/** _start_geometry **/',
                        '_start_geometry: %s,' % _safe_json(start_geometry))
    btl.response.content_type = 'application/javascript'
    _set_response_headers(btl.response)
    return page


@btl.route('/<path:path>')
def _static(path):
    response = None
    if 'jinja_env' in _start_args and 'jinja_templates' in _start_args:
        template_prefix = _start_args['jinja_templates'] + '/'
        if path.startswith(template_prefix):
            n = len(template_prefix)
            template = _start_args['jinja_env'].get_template(path[n:])
            response = btl.HTTPResponse(template.render())

    if response is None:
        response = btl.static_file(path, root=root_path)

    _set_response_headers(response)
    return response


@btl.get('/eel', apply=[wbs.websocket])
def _websocket(ws):
    global _websockets

    for js_function in _js_functions:
        _import_js_function(js_function)

    page = btl.request.query.page
    if page not in _mock_queue_done:
        for call in _mock_queue:
            _repeated_send(ws, _safe_json(call))
        _mock_queue_done.add(page)

    _websockets += [(page, ws)]

    while True:
        msg = ws.receive()
        if msg is not None:
            message = jsn.loads(msg)
            spawn(_process_message, message, ws)
        else:
            _websockets.remove((page, ws))
            break

    _websocket_close(page)

# Private functions

def _safe_json(obj):
    return jsn.dumps(obj, default=lambda o: None)


def _repeated_send(ws, msg):
    for attempt in range(100):
        try:
            ws.send(msg)
            break
        except Exception:
            sleep(0.001)


def _process_message(message, ws):
    if 'call' in message:
        return_val = _exposed_functions[message['name']](*message['args'])
        _repeated_send(ws, _safe_json({ 'return': message['call'],
                                        'value': return_val  }))
    elif 'return' in message:
        call_id = message['return']
        if call_id in _call_return_callbacks:
            callback = _call_return_callbacks.pop(call_id)
            callback(message['value'])
        else:
            _call_return_values[call_id] = message['value']
    else:
        print('Invalid message received: ', message)


def _get_real_path(path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.abspath(path)


def _mock_js_function(f):
    exec('%s = lambda *args: _mock_call("%s", args)' % (f, f), globals())


def _import_js_function(f):
    exec('%s = lambda *args: _js_call("%s", args)' % (f, f), globals())


def _call_object(name, args):
    global _call_number
    _call_number += 1
    call_id = _call_number + rnd.random()
    return {'call': call_id, 'name': name, 'args': args}


def _mock_call(name, args):
    call_object = _call_object(name, args)
    global _mock_queue
    _mock_queue += [call_object]
    return _call_return(call_object)


def _js_call(name, args):
    call_object = _call_object(name, args)
    for _, ws in _websockets:
        _repeated_send(ws, _safe_json(call_object))
    return _call_return(call_object)


def _call_return(call):
    call_id = call['call']

    def return_func(callback=None):
        if callback is not None:
            _call_return_callbacks[call_id] = callback
        else:
            for w in range(10000):
                if call_id in _call_return_values:
                    return _call_return_values.pop(call_id)
                sleep(0.001)
    return return_func


def _expose(name, function):
    msg = 'Already exposed function with name "%s"' % name
    assert name not in _exposed_functions, msg
    _exposed_functions[name] = function


def _websocket_close(page):
    close_callback = _start_args.get('close_callback')

    if close_callback is not None:
        sockets = [p for _, p in _websockets]
        close_callback(page, sockets)
    else:
        # Default behaviour - wait 1s, then quit if all sockets are closed
        sleep(1.0)
        if len(_websockets) == 0:
            sys.exit()


def _set_response_headers(response):
    if _start_args['disable_cache']:
        # https://stackoverflow.com/a/24748094/280852
        response.set_header('Cache-Control', 'no-store')
