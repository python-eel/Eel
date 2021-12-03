import os, random


import eel

eel.init('web')

@eel.expose
def pick_file(folder):
    if not os.path.isdir(folder):
        return 'Not a valid folder'

    files = os.listdir(folder)
        
    return random.choice(files)

eel.start('file_access.html', size=(320, 120))
