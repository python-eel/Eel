import sys
sys.path.insert(1, '../../')
# Use latest version of Eel from parent directory

import os
import platform

import eel

# Use the same static files as the original Example
os.chdir(os.path.join('..', '01 - hello_world'))

# Set web files folder and optionally specify which file types to check for eel.expose()
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

# Launch example in Microsoft Edge only on Windows 10 and above
if sys.platform in ['win32', 'win64'] and int(platform.release()) > 10:
    eel.start('hello.html', options={'mode': 'edge'})
else:
    raise EnvironmentError('Error: System is not Windows 10 or above')

# # Launching Edge can also be gracefully handled as a fall back
# try:
#     # Default call from `examples/01 - hello_world/`
#     eel.start('hello.html', size=(300, 200))
# except EnvironmentError:
#     # If Chrome isn't found, fallback to Microsoft Edge on Windows 10 or greater
#     if sys.platform in ['win32', 'win64'] and int(platform.release()) > 10:
#         eel.start('hello.html', options={'mode': 'edge'})
