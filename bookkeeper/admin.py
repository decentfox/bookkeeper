from decent.web.db import db
from flask import url_for
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.menu import MenuLink
from flask.ext.login import current_user

from . import models
from .views import (index, voucher, company, period)


# noinspection PyAbstractClass
class AnonymousLink(MenuLink):
    def is_accessible(self):
        return current_user.is_anonymous


# noinspection PyAbstractClass
class UserLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


class UserNameLink(UserLink):
    @property
    def name(self):
        return current_user.email

    @name.setter
    def name(self, val):
        pass

    def get_url(self):
        return url_for(self.endpoint, id=current_user.id)


class CompanyLink(MenuLink):
    @property
    def name(self):
        return current_user.current_company.name

    @name.setter
    def name(self, val):
        pass

    def is_accessible(self):
        return getattr(current_user, 'current_company', None) is not None


class PeriodLink(UserLink):
    @property
    def name(self):
        return str(current_user.current_period)

    @name.setter
    def name(self, val):
        pass


def init_app(app):
    admin = Admin(app=app, name='簿记员', url='/',
                  index_view=index.IndexView(url='/', menu_class_name='hide'),
                  template_mode='bootstrap3', base_template='base.html')
    admin.add_view(voucher.VoucherView(models.Voucher, db.session, '凭证'))
    admin.add_view(ModelView(
        models.Account, db.session, '科目', category='设置'))
    admin.add_view(ModelView(models.User, db.session, '用户', category='设置'))
    admin.add_view(ModelView(models.Role, db.session, '角色', category='设置'))
    admin.add_view(ModelView(
        models.CompanyRole, db.session, '角色分配', category='设置'))
    admin.add_view(company.CompanyView(
        models.Company, db.session, '公司', category='设置'))
    admin.add_view(
        period.PeriodView(models.Period, db.session, '账期', category='设置'))
    admin.add_link(AnonymousLink('登入', endpoint='security.login'))
    admin.add_link(PeriodLink('period', endpoint='period.index_view'))
    admin.add_link(CompanyLink('company', endpoint='company.index_view'))
    admin.add_link(UserNameLink('name', endpoint='user.edit_view'))
    admin.add_link(UserLink('登出', endpoint='security.logout'))
