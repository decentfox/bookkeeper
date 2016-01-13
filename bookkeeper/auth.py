from decent.web import db
from flask import redirect, url_for, request
from flask.ext.admin import helpers
from flask.ext.login import current_user
from flask.ext.security import SQLAlchemyUserDatastore, Security

from . import models

datastore = SQLAlchemyUserDatastore(db.db, models.User, models.Role)


class AuthOverride:
    def is_accessible(self):
        return current_user.is_active

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


def init(app):
    security = Security(app=app, datastore=datastore)

    @security.context_processor
    def security_context_processor():
        from .admin import admin
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
        )
