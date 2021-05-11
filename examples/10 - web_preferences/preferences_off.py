import eel

web_preferences = {
    'dev_tools': False,
    'context_menu': False,
    'property_does_not_exist': False  # Check is there is no runtime error for not existing key
}

eel.init('web')  # Set web files folder
eel.start('index.html', size=(600, 600), web_preferences=web_preferences)  # Start
