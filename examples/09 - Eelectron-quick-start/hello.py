import aal
# Set web files folder
aal.init('web')

@aal.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
aal.say_hello_js('Python World!')   # Call a Javascript function

aal.start('hello.html',mode='electron')
#aal.start('hello.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron.exe', '.'])
