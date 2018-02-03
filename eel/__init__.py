from __future__ import print_function
from builtins import range
from io import open
import json as jsn, bottle as btl, bottle.ext.websocket as wbs, gevent as gvt
import re as rgx, os, subprocess as sps, eel.browsers as brw, random as rnd, sys
import pkg_resources as pkg

_eel_js_file = pkg.resource_filename('eel', 'eel.js')
_eel_js = open(_eel_js_file, encoding='utf-8').read()
_websockets = []
_call_return_values = {}
_call_return_callbacks = {}
_call_number = 0
_exposed_functions = {}
_js_functions = []
_start_geometry = {}
_mock_queue = []
_mock_queue_done = set()
_default_options = {
    'mode': 'chrome-app',
    'host': 'localhost',
    'port': 8000,
    'chromeFlags': []
}

# Public functions

def expose(name_or_function = None):
    if name_or_function == None:    # Deal with '@eel.expose()' - treat as '@eel.expose'
        return expose
    
    if type(name_or_function) == str:   # Called as '@eel.expose("my_name")'
        name =  name_or_function
        def decorator(function):
            _expose(name, function)
            return function
        return decorator
    else:
        function = name_or_function
        _expose(function.__name__, function)
        return function
        
def init(path):
    global root_path, _js_functions
    root_path = _get_real_path(path)

    js_functions = set()
    for root, _, files in os.walk(root_path):
        for name in files:
            allowed_extensions = '.js .html .txt .htm .xhtml'.split()
            if not any(name.endswith(ext) for ext in allowed_extensions):
                continue
                
            try:
                with open(os.path.join(root, name), encoding='utf-8') as file:
                    contents = file.read()
                    expose_calls = set()
                    for expose_call in rgx.findall(r'eel\.expose\((.*)\)', contents):
                        expose_call = expose_call.strip()
                        assert rgx.findall(r'[\(=]', expose_call) == [], "eel.expose() call contains '(' or '='"
                        expose_calls.add(expose_call)
                    js_functions.update(expose_calls)
            except UnicodeDecodeError:
                pass    # Malformed file probably

    _js_functions = list(js_functions)
    for js_function in _js_functions:
        _mock_js_function(js_function)

def start(*start_urls, **kwargs):
    block = kwargs.pop('block', True)
    options = kwargs.pop('options', {})
    size = kwargs.pop('size', None)
    position = kwargs.pop('position', None)
    geometry = kwargs.pop('geometry', {})

    for k, v in list(_default_options.items()):
        if k not in options:
            options[k] = v
            
    _start_geometry['default'] = {'size': size, 'position': position}
    _start_geometry['pages'] = geometry
    
    brw.open(start_urls, options)

    run_lambda = lambda: btl.run(host=options['host'], port=options['port'], server=wbs.GeventWebSocketServer, quiet=True)
    if block:
        run_lambda()
    else:
        spawn(run_lambda)

def sleep(seconds):
    gvt.sleep(seconds)

def spawn(function):
    gvt.spawn(function)
    
# Bottle Routes

@btl.route('/eel.js')
def _eel():
    page = _eel_js.replace('/** _py_functions **/', '_py_functions: %s,' % list(_exposed_functions.keys()))
    page = page.replace('/** _start_geometry **/', '_start_geometry: %s,' % jsn.dumps(_start_geometry))
    return page
    
@btl.route('/<path:path>')
def _static(path):
    return btl.static_file(path, root=root_path)    

@btl.get('/eel', apply=[wbs.websocket])
def _websocket(ws):
    global _websockets
    _websockets += [ws]
    
    for js_function in _js_functions:
        _import_js_function(js_function)
    
    page = btl.request.query.page
    if page not in _mock_queue_done:
        for call in _mock_queue:
            ws.send(jsn.dumps(call))
        _mock_queue_done.add(page)
    
    while True:
        msg = ws.receive()
        if msg != None:
            message = jsn.loads(msg)
            if 'call' in message:
                return_val = _exposed_functions[message['name']](*message['args'])
                ws.send(jsn.dumps({'return': message['call'], 'value': return_val}))
            elif 'return' in message:
                call_id = message['return']
                if call_id in _call_return_callbacks:
                    callback = _call_return_callbacks.pop(call_id)
                    callback(message['value'])
                else:
                    _call_return_values[call_id] = message['value']
            else:
                print('Invalid message received: ', message)
        else:
            _websockets.remove(ws)            
            break
    
    _websocket_close()
            
# Private functions

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
    for ws in _websockets:
        ws.send(jsn.dumps(call_object))
    return _call_return(call_object)

def _call_return(call):
    call_id, name, args = call['call'], call['name'], call['args']
    def return_func(callback = None):
        if callback != None:
            _call_return_callbacks[call_id] = callback
        else:
            for w in range(10000):
                if call_id in _call_return_values:
                    return _call_return_values.pop(call_id)
                sleep(0.001)
    return return_func
    
def _expose(name, function):
    assert name not in _exposed_functions, 'Already exposed function with name "%s"' % name
    _exposed_functions[name] = function

def _websocket_close():
    # a websocket just closed
    # TODO: user definable behavior here
    sleep(1.0)
    if len(_websockets) == 0:
        sys.exit()

