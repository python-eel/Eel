import aal
import random

aal.init('web')

@aal.expose
def py_random():
    return random.random()

@aal.expose
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
aal.js_random()(print_num)

# Do the same with an inline callback
aal.js_random()(lambda n: print('Got this from Javascript:', n))

# Show error handling
aal.js_with_error()(print_num, print_num_failed)


aal.start('callbacks.html', size=(400, 300))

