import aal

aal.init('web')                     # Give folder containing web files

@aal.expose                         # Expose this function to Javascript
def handleinput(x):
    print('%s' % x)

aal.say_hello_js('connected!')   # Call a Javascript function

aal.start('main.html', size=(500, 200))    # Start
