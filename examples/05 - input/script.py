import eel

eel.init('web')                     # Give folder containing web files

@eel.expose                         # Expose this function to Javascript
def handleinput(x):
    print('%s' % x)

eel.say_hello_js('connected!')   # Call a Javascript function

eel.start('main.html', size=(500, 200))    # Start
