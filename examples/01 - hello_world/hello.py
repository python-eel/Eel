import aal

# Set web files folder
paling.init('web')

@paling.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
paling.say_hello_js('Python World!')   # Call a Javascript function

paling.start('hello.html', size=(300, 200))  # Start
