from decent.web import register_extension
from flask import Blueprint


@register_extension
def _init(app):
    from . import admin
    from . import models
    from . import config

    app.config.from_object(config)
    app.register_blueprint(Blueprint('bkr', __name__,
                                     static_url_path='/static/bkr',
                                     static_folder='static',
                                     template_folder='templates'))
    admin.admin.init_app(app)
