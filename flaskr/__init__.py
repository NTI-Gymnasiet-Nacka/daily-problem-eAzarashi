'''
GÄLLER HELA UPPGIFTEN!
Okej så det som hänt här är att jag har kopierat in ett färdigt program och modifierat det 
lite för att det ska göra det jag vill, dvs vara en chattjänst istället för en blogtjänst.
Det ända jag gjort mestadels själv är att försöka skapa en websocket, men mina försök än så 
länge har misslyckats och jag skulle behöva betydligt mer tid för att kunna slutföra detta 
vilket jag inte har. Därför kommer jag lämna in uppgiften som den är nu och satsa på att prestera
bättre i senare uppgifter i kursen.

run command: flask --app flaskr run --host=0.0.0.0
             flask --app flaskr run --debug
'''

import os

from flask import Flask
from .websockets_event import socketio
from .websockets_event import init_socketio
from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from . import auth
    from . import blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
