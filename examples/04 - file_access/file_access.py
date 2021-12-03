import os, random


import eel

eel.init('web')

@eel.expose
def pick_file(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)
        
        return random.choice(files)
    
    return 'Not a valid folder'

eel.start('file_access.html', size=(320, 120))
