import random

import aal

aal.init('web')                     # Give folder containing web files

@aal.expose
def py_random():
    return random.random()

@aal.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
aal.say_hello_js('Python World!')   # Call a Javascript function

aal.start('templates/hello.html', size=(300, 200), jinja_templates='templates')    # Start
