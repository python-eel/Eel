import sys
sys.path.insert(1, '../../')
# Use latest version of Eel from parent directory

import os

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

# Launch example in Microsoft Edge
eel.start('hello.html', options={'mode': 'edge'})

# # Launching Edge can also be handled from a callback
# try:
#     # Default call from `examples/01 - hello_world/`
#     eel.start('hello.html', size=(300, 200))
# except EnvironmentError as e:
# 	# If Chrome isn't found, fallback to Microsoft Edge on Windows
#     if sys.platform in ['win32', 'win64']:
#         try:
#         	eel.start('hello.html', options={'mode': 'edge'})
#         except:  # TODO: What is error message on non-Win10 systems?
#             raise
