"""__init__.py serves double duty: it contains the application factor, and it tells python that the flasktd directory should be treated as a package"""

import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY = 'dev',
            DATABSE = os.path.join(app.instance_path, 'flasktd.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if available
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # finally... a simple page that says hello
    @app.route('/hello')
    def hello():
        return("Hello, World!")

    return(app)