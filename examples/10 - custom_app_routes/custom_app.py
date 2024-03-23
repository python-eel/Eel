import aal
import bottle
# from beaker.middleware import SessionMiddleware

app = bottle.Bottle()
@app.route('/custom')
def custom_route():
    return 'Hello, World!'

aal.init('web')

# need to manually add eel routes if we are wrapping our Bottle instance with middleware
# aal.add_eel_routes(app)
# middleware = SessionMiddleware(app)
# aal.start('index.html', app=middleware)

aal.start('index.html', app=app)
