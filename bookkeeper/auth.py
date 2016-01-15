from decent.web import db
from flask import redirect, url_for, request
from flask.ext.admin import helpers
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, Permission, TypeNeed, Denial
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
    access_perms = TypeNeed('active'),
    create_perms = ()
    edit_perms = ()
    delete_perms = ()
    detail_perms = ()
    export_perms = ()
    access_denials = ()
    create_denials = ()
    edit_denials = ()
    delete_denials = ()
    detail_denials = TypeNeed('active'),
    export_denials = TypeNeed('active'),

    def is_accessible(self):
        return Permission(*self.access_perms).union(
            Denial(*self.access_denials)).can()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

    @property
    def can_create(self):
        return Permission(*self.create_perms).union(
            Denial(*self.create_denials)).can()

    @property
    def can_edit(self):
        return Permission(*self.edit_perms).union(
            Denial(*self.edit_denials)).can()

    @property
    def can_delete(self):
        return Permission(*self.delete_perms).union(
            Denial(*self.delete_denials)).can()

    @property
    def can_view_details(self):
        return Permission(*self.detail_perms).union(
            Denial(*self.detail_denials)).can()

    @property
    def can_export(self):
        return Permission(*self.export_perms).union(
            Denial(*self.export_denials)).can()


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.provides.update(current_user.all_needs())


def init(app):
    security = Security(app=app, datastore=datastore)
    security.principal.skip_static = True

    @security.context_processor
    def security_context_processor():
        admin = app.extensions['admin'][-1]
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
        )
