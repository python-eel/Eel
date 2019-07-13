import eel

# Set web files folder and optionally specify which file types to check for eel.expose()
eel.init('web')

# disable_cache now defaults to True so this isn't strictly necessary. Set it to False to enable caching.
eel.start('disable_cache.html', size=(300, 200), disable_cache=True)    # Start
