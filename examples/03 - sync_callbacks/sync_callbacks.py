import aal, random

aal.init('web')

@aal.expose
def py_random():
    return random.random()

aal.start('sync_callbacks.html', block=False, size=(400, 300))

# Synchronous calls must happen after start() is called

# Get result returned synchronously by 
# passing nothing in second brackets
#                   v
n = aal.js_random()()
print('Got this from Javascript:', n)

while True:
    aal.sleep(1.0)
