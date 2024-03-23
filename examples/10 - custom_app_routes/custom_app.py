import aal
import bottle
# from beaker.middleware import SessionMiddleware

app = bottle.Bottle()
@app.route('/custom')
def custom_route():
    return 'Hello, World!'

paling.init('web')

# need to manually add eel routes if we are wrapping our Bottle instance with middleware
# paling.add_eel_routes(app)
# middleware = SessionMiddleware(app)
# paling.start('index.html', app=middleware)

paling.start('index.html', app=app)
