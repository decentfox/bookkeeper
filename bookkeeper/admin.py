from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from decent.web.db import db

from . import models


admin = Admin(url='/', template_mode='bootstrap3')

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Company, db.session))
admin.add_view(ModelView(models.Period, db.session))
admin.add_view(ModelView(models.Account, db.session))
admin.add_view(ModelView(models.Voucher, db.session))
