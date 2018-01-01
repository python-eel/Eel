import eel, os, random

eel.init('web')

@eel.expose
def pick_file(folder):
    if os.path.isdir(folder):
        return random.choice(os.listdir(folder))
    else:
        return 'Not valid folder'

eel.start('file_access.html', size=(320, 120))
