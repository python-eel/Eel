import aal, random

paling.init('web')

@paling.expose
def py_random():
    return random.random()

paling.start('sync_callbacks.html', block=False, size=(400, 300))

# Synchronous calls must happen after start() is called

# Get result returned synchronously by 
# passing nothing in second brackets
#                   v
n = paling.js_random()()
print('Got this from Javascript:', n)

while True:
    paling.sleep(1.0)
