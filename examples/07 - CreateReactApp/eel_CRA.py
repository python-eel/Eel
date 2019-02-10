import sys
sys.path.insert(1, '../../')
# Use latest version of Eel from parent directory

import os
import random

import eel


@eel.expose                         # Expose this function to JavaScript
def say_hello_py(x):
    # Print to Python console
    print('Hello from %s' % x)
    # Call a JavaScript function
    eel.say_hello_js('Python {from within say_hello_py()}!')


@eel.expose
def pick_file(folder):
    folder = os.path.expanduser(folder)
    if os.path.isdir(folder):
        return random.choice(os.listdir(folder))
    else:
        return '{} is not a valid folder'.format(folder)


def start_eel(develop):
    """Start Eel with either production or development configuration"""
    if develop:
        directory = 'src'
        app = None
        page = {'port': 3000}
        flags = ['--auto-open-devtools-for-tabs']
    else:
        directory = 'build'
        app = 'chrome-app'
        page = 'index.html'
        flags = []

    eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])

    # These will be queued until the first connection is made, but won't be repeated on a page reload
    say_hello_py('Python World!')
    eel.say_hello_js('Python World!')   # Call a JavaScript function (must be after `eel.init()`)

    eelKArgs = {
        'size': (1280, 800),
        'options': {
            'mode': app,
            'port': 8080,
            'host': 'localhost',
            'chromeFlags': flags
        }
    }

    try:
        eel.start(page, **eelKArgs)
    except EnvironmentError:  # If Chrome isn't found, try Edge as a fall back
        if sys.platform in ['win32', 'win64']:
            eelKArgs['options']['mode'] = 'edge'
            try:
                eel.start(page, **eelKArgs)
            except:  # TODO: What is error message on non-Win10 systems?
                raise


if __name__ == '__main__':
    import sys

    # Pass any second argument to enable debugging. Production distribution can't receive arguments
    start_eel(develop=len(sys.argv) == 2)
