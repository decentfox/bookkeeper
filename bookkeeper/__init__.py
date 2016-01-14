from decent.web import DecentWeb
from flask import Flask
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.mail import Mail


def create_app():
    app = Flask(__name__)
    from . import config
    app.config.from_object(config)

    DecentWeb(app)

    from . import models
    from . import admin
    admin.admin.init_app(app)

    from . import auth
    auth.init(app)

    Mail(app)

    DebugToolbarExtension(app)

    return app
