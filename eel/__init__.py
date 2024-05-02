from builtins import range
import traceback
from io import open
from typing import Union, Any, Dict, List, Set, Tuple, Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from eel.types import OptionsDictT, WebSocketT
else:
    WebSocketT = Any
    OptionsDictT = Any

from gevent.threading import Timer
import gevent as gvt
import json as jsn
import bottle as btl
'''
Direct "import bottle websocket as wbs" (before update there is "import bottle.ext.websocket as wbs") 
to resolve the issue ModuleNotFoundError: No module named 'bottle.ext.websocket'

To verify the issue and the solution, please refer to the attached file: error-fix.md
'''
# Try to import bottle_websocket, if not found, import bottle.ext.websocket
try:
    import bottle_websocket as wbs
except ModuleNotFoundError:
    import bottle.ext.websocket as wbs
import re as rgx
import os
import eel.browsers as brw
import pyparsing as pp
import random as rnd
import sys
import pkg_resources as pkg
import socket
import mimetypes


mimetypes.add_type('application/javascript', '.js')
_eel_js_file: str = pkg.resource_filename('eel', 'eel.js')
_eel_js: str = open(_eel_js_file, encoding='utf-8').read()
_websockets: List[Tuple[Any, WebSocketT]] = []
_call_return_values: Dict[Any, Any] = {}
_call_return_callbacks: Dict[float, Tuple[Callable[..., Any], Optional[Callable[..., Any]]]] = {}
_call_number: int = 0
_exposed_functions: Dict[Any, Any] = {}
_js_functions: List[Any] = []
_mock_queue: List[Any] = []
_mock_queue_done: Set[Any] = set()
_shutdown: Optional[gvt.Greenlet] = None    # Later assigned as global by _websocket_close()
root_path: str                              # Later assigned as global by init()

# The maximum time (in milliseconds) that Python will try to retrieve a return value for functions executing in JS
# Can be overridden through `eel.init` with the kwarg `js_result_timeout` (default: 10000)
_js_result_timeout: int = 10000

# All start() options must provide a default value and explanation here
_start_args: OptionsDictT = {
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
    'default_path': 'index.html',                   # The default file to retrieve for the root URL
    'app': btl.default_app(),                       # Allows passing in a custom Bottle instance, e.g. with middleware
    'shutdown_delay': 1.0                           # how long to wait after a websocket closes before detecting complete shutdown
}

# == Temporary (suppressible) error message to inform users of breaking API change for v1.0.0 ===
_start_args['suppress_error'] = False
api_error_message: str = '''
----------------------------------------------------------------------------------
  'options' argument deprecated in v1.0.0, see https://github.com/ChrisKnott/Eel
  To suppress this error, add 'suppress_error=True' to start() call.
  This option will be removed in future versions
----------------------------------------------------------------------------------
'''
# ===============================================================================================

# Public functions

def expose(name_or_function: Optional[Callable[..., Any]] = None) -> Callable[..., Any]:
    # Deal with '@eel.expose()' - treat as '@eel.expose'
    if name_or_function is None:
        return expose

    if isinstance(name_or_function, str):   # Called as '@eel.expose("my_name")'
        name = name_or_function

        def decorator(function: Callable[..., Any]) -> Any:
            _expose(name, function)
            return function
        return decorator
    else:
        function = name_or_function
        _expose(function.__name__, function)
        return function


# PyParsing grammar for parsing exposed functions in JavaScript code
# Examples: `eel.expose(w, "func_name")`, `eel.expose(func_name)`, `eel.expose((function (e){}), "func_name")`
EXPOSED_JS_FUNCTIONS: pp.ZeroOrMore = pp.ZeroOrMore(
    pp.Suppress(
        pp.SkipTo(pp.Literal('eel.expose('))
        + pp.Literal('eel.expose(')
        + pp.Optional(
            pp.Or([pp.nestedExpr(), pp.Word(pp.printables, excludeChars=',')]) + pp.Literal(',')
        )
    )
    + pp.Suppress(pp.Regex(r'["\']?'))
    + pp.Word(pp.printables, excludeChars='"\')')
    + pp.Suppress(pp.Regex(r'["\']?\s*\)')),
)


def init(path: str, allowed_extensions: List[str] = ['.js', '.html', '.txt', '.htm',
                                   '.xhtml', '.vue'], js_result_timeout: int = 10000) -> None:
    global root_path, _js_functions, _js_result_timeout
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
                    matches = EXPOSED_JS_FUNCTIONS.parseString(contents).asList()
                    for expose_call in matches:
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

    _js_result_timeout = js_result_timeout


def start(*start_urls: str, **kwargs: Any) -> None:
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
        if not isinstance(_start_args['jinja_templates'], str):
            raise TypeError("'jinja_templates start_arg/option must be of type str'")
        templates_path = os.path.join(root_path, _start_args['jinja_templates'])
        _start_args['jinja_env'] = Environment(loader=FileSystemLoader(templates_path),
                                 autoescape=select_autoescape(['html', 'xml']))

    # verify shutdown_delay is correct value
    if not isinstance(_start_args['shutdown_delay'], (int, float)):
        raise ValueError("`shutdown_delay` must be a number, "\
            "got a {}".format(type(_start_args['shutdown_delay'])))

    # Launch the browser to the starting URLs
    show(*start_urls)

    def run_lambda() -> None:
        if _start_args['all_interfaces'] == True:
            HOST = '0.0.0.0'
        else:
            if not isinstance(_start_args['host'], str):
                raise TypeError("'host' start_arg/option must be of type str")
            HOST = _start_args['host']

        app = _start_args['app']

        if isinstance(app, btl.Bottle):
            register_eel_routes(app)
        else:
            register_eel_routes(btl.default_app())

        btl.run(
            host=HOST,
            port=_start_args['port'],
            server=wbs.GeventWebSocketServer,
            quiet=True,
            app=app) # Always returns None

    # Start the webserver
    if _start_args['block']:
        run_lambda()
    else:
        spawn(run_lambda)


def show(*start_urls: str) -> None:
    brw.open(list(start_urls), _start_args)


def sleep(seconds: Union[int, float]) -> None:
    gvt.sleep(seconds)


def spawn(function: Callable[..., Any], *args: Any, **kwargs: Any) -> gvt.Greenlet:
    return gvt.spawn(function, *args, **kwargs)

# Bottle Routes

def _eel() -> str:
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

def _root() -> Optional[btl.Response]:
    if not isinstance(_start_args['default_path'], str):
        raise TypeError("'default_path' start_arg/option must be of type str")
    return _static(_start_args['default_path'])

def _static(path: str) -> Optional[btl.Response]:
    response = None
    if 'jinja_env' in _start_args and 'jinja_templates' in _start_args:
        if not isinstance(_start_args['jinja_templates'], str):
            raise TypeError("'jinja_templates' start_arg/option must be of type str")
        template_prefix = _start_args['jinja_templates'] + '/'
        if path.startswith(template_prefix):
            n = len(template_prefix)
            template = _start_args['jinja_env'].get_template(path[n:]) # type: ignore # depends on conditional import in start()
            response = btl.HTTPResponse(template.render())

    if response is None:
        response = btl.static_file(path, root=root_path)

    _set_response_headers(response)
    return response

def _websocket(ws: WebSocketT) -> None:
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


BOTTLE_ROUTES: Dict[str, Tuple[Callable[..., Any], Dict[Any, Any]]] = {
    "/eel.js": (_eel, dict()),
    "/": (_root, dict()),
    "/<path:path>": (_static, dict()),
    "/eel": (_websocket, dict(apply=[wbs.websocket]))
}

def register_eel_routes(app: btl.Bottle) -> None:
    '''
    Adds eel routes to `app`. Only needed if you are passing something besides `bottle.Bottle` to `eel.start()`.
    Ex:
    app = bottle.Bottle()
    eel.register_eel_routes(app)
    middleware = beaker.middleware.SessionMiddleware(app)
    eel.start(app=middleware)
    '''
    for route_path, route_params in BOTTLE_ROUTES.items():
        route_func, route_kwargs = route_params
        app.route(path=route_path, callback=route_func, **route_kwargs)

# Private functions

def _safe_json(obj: Any) -> str:
    return jsn.dumps(obj, default=lambda o: None)


def _repeated_send(ws: WebSocketT, msg: str) -> None:
    for attempt in range(100):
        try:
            ws.send(msg)
            break
        except Exception:
            sleep(0.001)


def _process_message(message: Dict[str, Any], ws: WebSocketT) -> None:
    if 'call' in message:
        error_info = {}
        try:
            return_val = _exposed_functions[message['name']](*message['args'])
            status = 'ok'
        except Exception as e:
            err_traceback = traceback.format_exc()
            traceback.print_exc()
            return_val = None
            status = 'error'
            error_info['errorText'] = repr(e)
            error_info['errorTraceback'] = err_traceback
        _repeated_send(ws, _safe_json({ 'return': message['call'],
                                        'status': status,
                                        'value': return_val,
                                        'error': error_info,}))
    elif 'return' in message:
        call_id = message['return']
        if call_id in _call_return_callbacks:
            callback, error_callback = _call_return_callbacks.pop(call_id)
            if message['status'] == 'ok':
                callback(message['value'])
            elif message['status'] == 'error' and error_callback is not None:
                error_callback(message['error'], message['stack'])
        else:
            _call_return_values[call_id] = message['value']

    else:
        print('Invalid message received: ', message)


def _get_real_path(path: str) -> str:
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, path) # type: ignore # sys._MEIPASS is dynamically added by PyInstaller
    else:
        return os.path.abspath(path)


def _mock_js_function(f: str) -> None:
    exec('%s = lambda *args: _mock_call("%s", args)' % (f, f), globals())


def _import_js_function(f: str) -> None:
    exec('%s = lambda *args: _js_call("%s", args)' % (f, f), globals())


def _call_object(name: str, args: Any) -> Dict[str, Any]:
    global _call_number
    _call_number += 1
    call_id = _call_number + rnd.random()
    return {'call': call_id, 'name': name, 'args': args}


def _mock_call(name: str, args: Any) -> Callable[[Optional[Callable[..., Any]], Optional[Callable[..., Any]]], Any]:
    call_object = _call_object(name, args)
    global _mock_queue
    _mock_queue += [call_object]
    return _call_return(call_object)


def _js_call(name: str, args: Any) -> Callable[[Optional[Callable[..., Any]], Optional[Callable[..., Any]]], Any]:
    call_object = _call_object(name, args)
    for _, ws in _websockets:
        _repeated_send(ws, _safe_json(call_object))
    return _call_return(call_object)


def _call_return(call: Dict[str, Any]) -> Callable[[Optional[Callable[..., Any]], Optional[Callable[..., Any]]], Any]:
    global _js_result_timeout
    call_id = call['call']

    def return_func(callback: Optional[Callable[..., Any]] = None,
                    error_callback: Optional[Callable[..., Any]] = None) -> Any:
        if callback is not None:
            _call_return_callbacks[call_id] = (callback, error_callback)
        else:
            for w in range(_js_result_timeout):
                if call_id in _call_return_values:
                    return _call_return_values.pop(call_id)
                sleep(0.001)
    return return_func


def _expose(name: str, function: Callable[..., Any]) -> None:
    msg = 'Already exposed function with name "%s"' % name
    assert name not in _exposed_functions, msg
    _exposed_functions[name] = function


def _detect_shutdown() -> None:
    if len(_websockets) == 0:
        sys.exit()


def _websocket_close(page: str) -> None:
    global _shutdown

    close_callback = _start_args.get('close_callback')

    if close_callback is not None:
        if not callable(close_callback):
            raise TypeError("'close_callback' start_arg/option must be callable or None")
        sockets = [p for _, p in _websockets]
        close_callback(page, sockets)
    else:
        if isinstance(_shutdown, gvt.Greenlet):
            _shutdown.kill()

        _shutdown = gvt.spawn_later(_start_args['shutdown_delay'], _detect_shutdown)


def _set_response_headers(response: btl.Response) -> None:
    if _start_args['disable_cache']:
        # https://stackoverflow.com/a/24748094/280852
        response.set_header('Cache-Control', 'no-store')
