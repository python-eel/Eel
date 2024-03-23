import aal

# Set web files folder and optionally specify which file types to check for paling.expose()
paling.init('web')

# disable_cache now defaults to True so this isn't strictly necessary. Set it to False to enable caching.
paling.start('disable_cache.html', size=(300, 200), disable_cache=True)    # Start
