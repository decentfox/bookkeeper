from decent.web.db import db
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.menu import MenuLink
from flask.ext.login import current_user

from . import models
from .views import (index, voucher)

admin = Admin(name='簿记员', url='/',
              index_view=index.IndexView(url='/', menu_class_name='hide'),
              template_mode='bootstrap3', base_template='base.html')

admin.add_view(voucher.VoucherView(models.Voucher, db.session, '凭证'))
admin.add_view(ModelView(models.Account, db.session, '科目', category='设置'))
admin.add_view(ModelView(models.User, db.session, '用户', category='设置'))
admin.add_view(ModelView(models.Company, db.session, '公司', category='设置'))
admin.add_view(ModelView(models.Period, db.session, '账期', category='设置'))


# noinspection PyAbstractClass
class AnonymousLink(MenuLink):
    def is_accessible(self):
        return current_user.is_anonymous


# noinspection PyAbstractClass
class UserLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


admin.add_link(AnonymousLink('登入', endpoint='security.login'))
admin.add_link(UserLink('登出', endpoint='security.logout'))
