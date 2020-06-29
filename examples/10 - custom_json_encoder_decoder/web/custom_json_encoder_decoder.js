eel.expose(js_json_data_sender);
function js_json_data_sender() {
    return {
        datetime: new Date()
    }
}

function print_value(v) {
    console.log('Got this value from python:');
    console.log(v);
}

// Call Python function.
eel.py_json_data_sender()(print_value);

// Call JS function from python.
eel.py_json_data_loader();
