import eel
import random

eel.init('web')

@eel.expose
def py_random():
    return random.random()

@eel.expose
def py_exception(error):
    if error:
        raise ValueError("Test")
    else:
        return "No Error"

def print_num(n):
    print('Got this from Javascript:', n)


def print_num_failed(error, stack):
    print("This is an example of what javascript errors would look like:")
    print("\tError: ", error)
    print("\tStack: ", stack)

# Call Javascript function, and pass explicit callback function    
eel.js_random()(print_num)

# Do the same with an inline callback
eel.js_random()(lambda n: print('Got this from Javascript:', n))

# Show error handling
eel.js_with_error()(print_num, print_num_failed)


eel.start('callbacks.html', size=(400, 300))

