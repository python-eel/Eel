import eel

# Set web files folder
eel.init('web')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function


options = {
	'mode': 'custom',
	'args': ['node_modules/electron/dist/electron.exe', '.']
}

eel.start('hello.html', options=options)
#eel.start('hello.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron.exe', '.'])
