import os
import sys

# Use latest version of Eel from parent directory
sys.path.insert(1, '../../')
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

# Set parameters irrespective of browser choice
start_page = 'hello.html'
window_size = (300, 200)
# Launch example in Microsoft Edge if found
try:
    eel.start(start_page, mode='edge', size=window_size)
except EnvironmentError as exc1:
    # If Edge isn't found, attempt fallback to Chrome or raise error
    try:
        print("Try chrome...")
        eel.start(start_page, mode='chrome', size=window_size)
    except EnvironmentError as exc2:
        raise EnvironmentError(f'{exc1} AND {exc2}')
