from decent.web import DecentWeb
from flask import Flask, g
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.mail import Mail
from flask.ext.principal import AnonymousIdentity


def create_app():
    app = Flask(__name__)
    from . import config
    app.config.from_object(config)

    DecentWeb(app)

    from . import models

    from . import auth
    auth.init(app)

    from . import admin
    with app.app_context():
        g.identity = AnonymousIdentity()
        admin.init_app(app)

    Mail(app)

    DebugToolbarExtension(app)

    return app
