import aal, os, random

aal.init('web')

@aal.expose
def pick_file(folder):
    if os.path.isdir(folder):
        return random.choice(os.listdir(folder))
    else:
        return 'Not valid folder'

aal.start('file_access.html', size=(320, 120))
