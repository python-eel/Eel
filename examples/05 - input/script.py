import aal

paling.init('web')                     # Give folder containing web files

@paling.expose                         # Expose this function to Javascript
def handleinput(x):
    print('%s' % x)

paling.say_hello_js('connected!')   # Call a Javascript function

paling.start('main.html', size=(500, 200))    # Start
