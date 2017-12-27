import json as jsn, bottle as btl, bottle.ext.websocket as wbs, gevent as gvt
import re as rgx, os, subprocess as sps, eel.browsers as brw, random as rnd

_eel_js_file = os.path.join(os.path.dirname(__file__), 'eel.js')
_eel_js = open(_eel_js_file, encoding='utf8').read()
_websockets = []
_call_return_values = {}
_call_return_callbacks = {}
_call_number = 0
_exposed_functions = {}
_js_functions = []
_mock_queue = []
_default_options = {
    'mode': 'chrome-app',
    'host': 'localhost',
    'port': 8000
}

# Public functions

def expose(name_or_function = None):
    if name_or_function == None:
        return expose
    
    if type(name_or_function) == str:
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
    root_path = path

    js_functions = set()
    for root, _, files in os.walk(root_path):
        for name in files:
            try:
                with open(os.path.join(root, name), encoding='utf8') as file:                
                    contents = file.read()
                    expose_calls = rgx.findall(r'eel\.expose\((.*)\)', contents)
                    js_functions.update(set(expose_calls))
            except UnicodeDecodeError:
                pass    # Probably an image

    _js_functions = list(js_functions)
    for js_function in _js_functions:
        _mock_js_function(js_function)

def start(*start_urls, block=True, options={}):
    for k, v in _default_options.items():
        if k not in options:
            options[k] = v

    brw.open(start_urls, options)

    run_lambda = lambda: btl.run(host=options['host'], port=options['port'], server=wbs.GeventWebSocketServer, quiet=True)
    if block:
        run_lambda()
    else:
        gvt.spawn(run_lambda)

def sleep(seconds):
    gvt.sleep(seconds)

# Bottle Routes

@btl.route('/eel.js')
def _eel():
    function_names = list(_exposed_functions.keys())
    return _eel_js.replace('/** _py_functions **/', '_py_functions: %s,' % function_names)
    
@btl.route('/<path:path>')
def _static(path):
    if root_path is None:
        return 'Initialising...'
    
    return btl.static_file(path, root=root_path)    

@btl.get('/eel', apply=[wbs.websocket])
def _websocket(ws):
    global _websockets
    _websockets += [ws]
    
    for js_function in _js_functions:
        _import_js_function(js_function)
    
    while _mock_queue != []:
        # TODO: pages should open websocket with their window.location
        #       then don't pop, send whole mock queue to each page once only
        call = _mock_queue.pop(0);
        ws.send(jsn.dumps(call))

    while True:
        msg = ws.receive()
        if msg != None:
            message = jsn.loads(msg)
            #print(message)
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
            
# Private functions

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
    if name in _exposed_functions:
        raise RuntimeError('Already exposed function with name "%s"' % name)
    _exposed_functions[name] = function


        