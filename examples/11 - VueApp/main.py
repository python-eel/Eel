import eel

eel.init('web/dist') 

@eel.expose
def say_hello(name):
    print(f"Python says: Hello, {name}!")
    return f"Hello, {name}! This is Python."

eel.start('index.html', mode='edge')
