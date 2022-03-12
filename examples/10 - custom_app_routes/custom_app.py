import eel
import bottle
from beaker.middleware import SessionMiddleware

app = bottle.Bottle()
@app.route('/custom')
def custom_route():
    return 'Hello, World!'

# need to manually add eel routes if we are wrapping our Bottle instance with middleware
eel.add_eel_routes(app)
middleware = SessionMiddleware(app)

eel.init('web')
eel.start('index.html', app=middleware)