import eel

web_preferences = {
    'dev_tools': True,
    'context_menu': True,
    'property_does_not_exist': True  # Check is there is no runtime error for not existing key
}

eel.init('web')  # Set web files folder
eel.start('index.html', size=(600, 600), web_preferences=web_preferences)  # Start
