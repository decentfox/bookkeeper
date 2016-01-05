from decent.web import register_extension


@register_extension
def _init(app):
    from . import admin
    from . import models
    from . import config

    app.config.from_object(config)
    admin.admin.init_app(app)
