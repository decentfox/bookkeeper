from decent.web.db import db
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

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
