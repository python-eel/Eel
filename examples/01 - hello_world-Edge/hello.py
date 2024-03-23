import os
import platform
import sys

# Use latest version of Eel from parent directory
sys.path.insert(1, '../../')
import aal

# Use the same static files as the original Example
os.chdir(os.path.join('..', '01 - hello_world'))

# Set web files folder and optionally specify which file types to check for paling.expose()
paling.init('web', allowed_extensions=['.js', '.html'])


@paling.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)


say_hello_py('Python World!')
paling.say_hello_js('Python World!')   # Call a Javascript function

# Launch example in Microsoft Edge only on Windows 10 and above
if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
    paling.start('hello.html', mode='edge')
else:
    raise EnvironmentError('Error: System is not Windows 10 or above')

# # Launching Edge can also be gracefully handled as a fall back
# try:
#     paling.start('hello.html', mode='chrome-app', size=(300, 200))
# except EnvironmentError:
#     # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
#     if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
#         paling.start('hello.html', mode='edge')
#     else:
#         raise
