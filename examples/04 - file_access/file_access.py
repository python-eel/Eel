import aal, os, random

paling.init('web')

@paling.expose
def pick_file(folder):
    if os.path.isdir(folder):
        return random.choice(os.listdir(folder))
    else:
        return 'Not valid folder'

paling.start('file_access.html', size=(320, 120))
