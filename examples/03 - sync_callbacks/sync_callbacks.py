import eel, random

eel.init('web')

@eel.expose
def py_random():
    return random.random()

eel.start('sync_callbacks.html', block=False, size=(400, 300))

# Synchronous calls must happen after start() is called

# Get result returned synchronously by 
# passing nothing in second brackets
#                   v
n = eel.js_random()()
print('Got this from Javascript:', n)

while True:
    eel.sleep(1.0)
