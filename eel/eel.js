class Eel {
    #host = window.location.origin;

    set_host(hostname) { this.#host = hostname; }

    expose(func, name) {
        if (name === undefined) {
            name = func.toString();
            const i = 'function '.length;
            const j = name.indexOf('(');
            name = name.substring(i, j).trim();
        }
        this.#exposed_functions[name] = func;
    }

    guid = () => this.#guid;

    constructor() { this.#init(); }

    #py_functions // Injected by Python

    #start_geometry // Injected by Python

    #guid = ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, char =>
        (char ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> char / 4)
            .toString(16)
    );

    #exposed_functions = {};

    #mock_queue = [];

    #mock_py_functions() {
        for (let i = 0; i < this.#py_functions.length; i++) {
            const name = this.#py_functions[i];
            this[name] = function() {
                const call_object = this.#call_object(name, arguments);
                this.#mock_queue.push(call_object);
                return this.#call_return(call_object);
            }
        }
    }

    #import_py_function(name) {
        this[name] = function() {
            const call_object = this.#call_object(name, arguments);
            this.#websocket.send(this.#to_json(call_object));
            return this.#call_return(call_object);
        }
    }

    #call_number = 0;

    #call_return_callbacks = {};

    #call_object(name, args) {
        const arg_array = [];
        for (let i = 0; i < args.length; i++)
            arg_array.push(args[i]);
        const call_id = (this.#call_number += 1) + Math.random();
        return {'call': call_id, 'name': name, 'args': arg_array};
    }

    #sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    #to_json(obj) {
        return JSON.stringify(obj, (_key, value) =>
            value === undefined ? null : value
        );
    }

    #call_return(call) {
        return (callback = null) => {
            if (callback !== null)
                this.#call_return_callbacks[call.call] = {resolve: callback};
            else
                return new Promise((resolve, reject) =>
                    this.#call_return_callbacks[call.call] = {resolve, reject}
                );
        }
    }

    #position_window(page) {
        let size = this.#start_geometry['default'].size;
        let position = this.#start_geometry['default'].position;
        if (page in this.#start_geometry.pages) {
            size = this.#start_geometry.pages[page].size;
            position = this.#start_geometry.pages[page].position;
        }
        if (size !== null)
            window.resizeTo(size[0], size[1]);
        if (position !== null)
            window.moveTo(position[0], position[1]);
    }

    #websocket;

    #init() {
        this.#mock_py_functions();

        document.addEventListener("DOMContentLoaded", (_event) => {
            const page = window.location.pathname.substring(1);
            this.#position_window(page);

            const websocket_addr =
                (this.#host + '/eel').replace('http', 'ws') + ('?page=' + page);
            this.#websocket = new WebSocket(websocket_addr);

            this.#websocket.onopen = () => {
                for (let i = 0; i < this.#py_functions.length; i++) {
                    const py_function = this.#py_functions[i];
                    this.#import_py_function(py_function);
                }
                while (this.#mock_queue.length > 0) {
                    const call = this.#mock_queue.shift();
                    this.#websocket.send(this.#to_json(call));
                }
            };

            this.#websocket.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                if (msg.hasOwnProperty('call')) {
                    if (msg.name in this.#exposed_functions) {
                        // Python making a function call into us
                        try {
                            const returned_value =
                                this.#exposed_functions[msg.name](...msg.args);
                            this.#websocket.send(this.#to_json({
                                'return': msg.call,
                                'status': 'ok',
                                'value': returned_value
                            }));
                        } catch (error) {
                            this.#websocket.send(this.#to_json({
                                'return': msg.call,
                                'status': 'error',
                                'error': error.message,
                                'stack': error.stack
                            }));
                        }
                    }
                } else
                if (msg.hasOwnProperty('return'))
                    // Python returning a value to us
                    if (msg['return'] in this.#call_return_callbacks) {
                        const callback =
                            this.#call_return_callbacks[msg['return']];
                        const status = msg['status'];
                        if (status === 'ok')
                            callback.resolve(msg.value);
                        else
                        if (status === 'error' && callback.reject)
                            callback.reject(msg['error']);
                        delete this.#call_return_callbacks[msg['return']];
                    }
                else
                    throw 'Invalid message ' + msg;
            };
        });
    }
}

const eel = new Eel();

if (typeof require !== 'undefined') {
    // Avoid name collisions when using Electron, so jQuery etc work normally
    window.nodeRequire = require;
    delete window.require;
    delete window.exports;
    delete window.module;
}
