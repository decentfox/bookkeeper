from flask import request, redirect, url_for
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.model.helpers import get_mdict_item_or_list
from flask.ext.login import current_user
from flask.ext.principal import Denial, RoleNeed

from ..auth import AuthOverride


class CompanyView(AuthOverride, ModelView):
    list_template = 'company_list.html'

    def get_query(self):
        rv = super().get_query()
        if Denial(RoleNeed('super')).can():
            rv = rv.filter(self.model.users.contains(current_user))
        return rv

    def get_count_query(self):
        rv = super().get_count_query()
        if Denial(RoleNeed('super')).can():
            rv = rv.filter(self.model.users.contains(current_user))
        return rv

    @expose('/switch/')
    def switch_view(self):
        id = get_mdict_item_or_list(request.args, 'id')
        current_user.current_company = id
        return redirect(url_for('.index_view'))
