eel = {
    expose: function(f, name) {
        if(name === undefined){
            name = f.toString();
            let i = 'function '.length, j = name.indexOf('(');
            name = name.substring(i, j).trim();
        }
        
        eel._exposed_functions[name] = f;
    },
    
    // These get dynamically added by library when file is served
    /** _py_functions **/
    /** _start_geometry **/

    _exposed_functions: {},
        
    _mock_queue: [],
    
    _mock_py_functions: function() {
        for(let i = 0; i < eel._py_functions.length; i++) {
            let name = eel._py_functions[i];
            eel[name] = function() {
                let call_object = eel._call_object(name, arguments);
                eel._mock_queue.push(call_object);
                return eel._call_return(call_object);
            }
        }
    },
    
    _import_py_function: function(name) {
        let func_name = name;
        eel[name] = function() {
            let call_object = eel._call_object(func_name, arguments);
            eel._websocket.send(eel._toJSON(call_object));
            return eel._call_return(call_object);
        }
    },
    
    _call_number: 0,
    
    _call_return_callbacks: {},
    
    _call_object: function(name, args) {
        let arg_array = [];
        for(let i = 0; i < args.length; i++){
            arg_array.push(args[i]);
        }
        
        let call_id = (eel._call_number += 1) + Math.random();
        return {'call': call_id, 'name': name, 'args': arg_array};
    },
    
    _sleep: function(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },
    
    _toJSON: function(obj) {
        return JSON.stringify(obj, (k, v) => v === undefined ? null : v);
    },
    
    _call_return: function(call) {
        return function(callback = null) {
            if(callback != null) {
                eel._call_return_callbacks[call.call] = callback;
            } else {
                return new Promise(function(resolve) {
                    eel._call_return_callbacks[call.call] = resolve;
                });
            }
        }
    },
    
    _position_window: function(page) {
        let size = eel._start_geometry['default'].size;
        let position = eel._start_geometry['default'].position;
        
        if(page in eel._start_geometry.pages) {
            size = eel._start_geometry.pages.size;
            position = eel._start_geometry.pages.position;
        }
        
        if(size != null){
            window.resizeTo(size[0], size[1]);
        }
        
        if(position != null){
            window.moveTo(position[0], position[1]);
        }        
    },
    
    _init: function() {
        eel._mock_py_functions();
        
        document.addEventListener("DOMContentLoaded", function(event) {
            let page = window.location.pathname.substring(1);
            eel._position_window(page);
            
            let websocket_addr = (window.location.origin + '/eel').replace('http', 'ws');
            websocket_addr += ('?page=' + page);
            eel._websocket = new WebSocket(websocket_addr);
            
            eel._websocket.onopen = function() {
                for(let i = 0; i < eel._py_functions.length; i++){
                    let py_function = eel._py_functions[i];
                    eel._import_py_function(py_function);
                }
                
                while(eel._mock_queue.length > 0) {
                    let call = eel._mock_queue.shift();
                    eel._websocket.send(eel._toJSON(call));
                }
            };
            
            eel._websocket.onmessage = function (e) {
                let message = JSON.parse(e.data);
                if(message.hasOwnProperty('call') ) {
                    // Python making a function call into us
                    if(message.name in eel._exposed_functions) {
                        let return_val = eel._exposed_functions[message.name](...message.args);
                        eel._websocket.send(eel._toJSON({'return': message.call, 'value': return_val}));
                    }
                } else if(message.hasOwnProperty('return')) {
                    // Python returning a value to us
                    if(message['return'] in eel._call_return_callbacks) {
                        eel._call_return_callbacks[message['return']](message.value);
                    }
                } else {
                    throw 'Invalid message ' + message;
                }
                
            };
        });
    }
}

eel._init();