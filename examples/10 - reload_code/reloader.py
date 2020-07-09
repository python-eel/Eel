import eel

eel.init("web")


@eel.expose
def updating_message():
    return "Change this message in `reloader.py` and see it available in the browser after a few seconds/clicks."


eel.start("reloader.html", size=(320, 120), reload_python_on_change=True)
