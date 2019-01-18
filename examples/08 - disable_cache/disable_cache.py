import eel

# Set web files folder and optionally specify which file types to check for eel.expose()
eel.init('web')
eel.start('disable_cache.html', size=(300, 200), disable_cache=True)    # Start
