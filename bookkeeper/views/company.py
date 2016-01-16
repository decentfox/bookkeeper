from flask import request, redirect, url_for, g
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.model.helpers import get_mdict_item_or_list
from flask.ext.login import current_user
from flask.ext.principal import Denial, Permission

from .. import const
from .. import models
from ..auth import AuthOverride


class CompanyView(AuthOverride, ModelView):
    list_template = 'company_list.html'
    delete_perms = const.P_SUPER_ADMIN,
    form_columns = ['name']

    def get_query(self):
        rv = super().get_query()
        if Denial(const.P_SUPER_ADMIN).can():
            rv = rv.filter(models.CompanyRole.query.filter(
                models.CompanyRole.company_id == self.model.id,
                models.CompanyRole.user == current_user,
            ).exists())
        return rv

    def get_count_query(self):
        rv = super().get_count_query()
        if Denial(const.P_SUPER_ADMIN).can():
            rv = rv.filter(models.CompanyRole.query.filter(
                models.CompanyRole.company_id == self.model.id,
                models.CompanyRole.user == current_user,
                ).exists())
        return rv

    @property
    def can_edit(self):
        row = getattr(g, 'company_view_row', None)
        if row is not None:
            return Permission(
                const.P_SUPER_ADMIN,
                const.P_COMPANY_ADMIN(row.id),
            ).can()
        return False

    @expose('/')
    def index_view(self):
        self._template_args['setattr'] = setattr
        return super().index_view()

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        g.company_view_row = self.get_one(
            get_mdict_item_or_list(request.args, 'id'))
        return super().edit_view()

    def on_model_change(self, form, model, is_created):
        if is_created:
            models.CompanyRole.create(
                commit=False, user=current_user, company=model,
                role=models.Role.get_by_need(const.P_ADMIN))

    @expose('/switch/')
    def switch_view(self):
        id_ = int(get_mdict_item_or_list(request.args, 'id'))
        current_user.current_company = id_
        return redirect(url_for('.index_view'))
