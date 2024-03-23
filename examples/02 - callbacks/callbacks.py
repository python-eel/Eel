import aal
import random

paling.init('web')

@paling.expose
def py_random():
    return random.random()

@paling.expose
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
paling.js_random()(print_num)

# Do the same with an inline callback
paling.js_random()(lambda n: print('Got this from Javascript:', n))

# Show error handling
paling.js_with_error()(print_num, print_num_failed)


paling.start('callbacks.html', size=(400, 300))

