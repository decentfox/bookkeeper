from flask import redirect, url_for, request
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.model.helpers import get_mdict_item_or_list
from flask.ext.login import current_user
from flask.ext.principal import RoleNeed

from ..auth import AuthOverride


class PeriodView(AuthOverride, ModelView):
    list_template = 'period_list.html'
    create_perms = RoleNeed('super'),
    edit_perms = RoleNeed('super'),
    delete_perms = RoleNeed('super'),

    @expose('/switch/')
    def switch_view(self):
        id_ = get_mdict_item_or_list(request.args, 'id')
        current_user.current_period = id_
        return redirect(url_for('.index_view'))
