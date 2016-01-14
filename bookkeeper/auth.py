from decent.web import db
from flask import redirect, url_for, request
from flask.ext.admin import helpers
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded
from flask.ext.security import SQLAlchemyUserDatastore, Security

from . import models


class CachedDatastore(SQLAlchemyUserDatastore):
    def find_user(self, **kwargs):
        if list(kwargs.keys()) == ['id']:
            return self.user_model.get_by_id(kwargs['id'])
        else:
            return super().find_user(**kwargs)


datastore = CachedDatastore(db.db, models.User, models.Role)


class AuthOverride:
    def is_accessible(self):
        return current_user.is_active

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.provides.update(current_user.all_needs())


def init(app):
    security = Security(app=app, datastore=datastore)
    security.principal.skip_static = True

    @security.context_processor
    def security_context_processor():
        from .admin import admin
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
        )
