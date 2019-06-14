from __future__ import print_function	# For Py2/3 compatibility
import eel

eel.init('web')                     # Give folder containing web files

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start('templates/hello.html', size=(300, 200), jinja_templates='templates')    # Start
