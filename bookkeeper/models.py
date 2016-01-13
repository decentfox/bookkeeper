from enum import IntEnum

import datetime
import sqlalchemy as sa
from decent.web import db
from flask.ext.security import RoleMixin, UserMixin
from sqlalchemy_utils import ChoiceType


class Direction(IntEnum):
    debit = 1
    credit = -1


Direction.debit.label = '借'
Direction.credit.label = '贷'

users_x_companies = sa.Table(
    'bkr_users_x_companies', db.Model.metadata,
    sa.Column('users_id', sa.BigInteger(), sa.ForeignKey('bkr_users.id')),
    sa.Column('companies_id', sa.BigInteger(),
              sa.ForeignKey('bkr_companies.id')),
)


roles_x_users = sa.Table(
    'bkr_users_x_roles', db.Model.metadata,
    sa.Column('users_id', sa.BigInteger(), sa.ForeignKey('bkr_users.id')),
    sa.Column('roles_id', sa.BigInteger(), sa.ForeignKey('bkr_roles.id')),
)


class User(db.Model, db.SurrogatePK, UserMixin):
    __tablename__ = 'bkr_users'

    companies = db.relationship(
        'Company', secondary=users_x_companies, backref='users')
    email = db.Column(sa.Unicode(), unique=True)
    password = db.Column(sa.Unicode())
    active = db.Column(sa.Boolean())
    confirmed_at = db.Column(sa.DateTime())
    last_login_at = db.Column(sa.DateTime())
    current_login_at = db.Column(sa.DateTime())
    last_login_ip = db.Column(sa.Unicode())
    current_login_ip = db.Column(sa.Unicode())
    login_count = db.Column(sa.BigInteger())
    roles = db.relationship('Role', secondary=roles_x_users, backref='users')


class Role(db.Model, db.SurrogatePK, RoleMixin):
    __tablename__ = 'bkr_roles'

    name = db.Column(sa.Unicode(), unique=True)
    description = db.Column(sa.Unicode())


class Company(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_companies'

    name = db.Column(sa.Unicode())

    def __repr__(self):
        return self.name


class Period(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_periods'

    year = db.Column(sa.Integer())
    month = db.Column(sa.SmallInteger())

    def __repr__(self):
        return '{}年第{}期'.format(self.year, self.month)


class Account(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_accounts'

    id = db.Column(sa.BigInteger(), primary_key=True)
    code = db.Column(sa.Unicode(), unique=True)
    title = db.Column(sa.Unicode(), nullable=False)
    direction = db.Column(ChoiceType(Direction, sa.SmallInteger()),
                          nullable=False, default=Direction.debit)

    parent_id = db.reference_col('bkr_accounts', nullable=True)
    parent = db.relationship('Account', backref='children',
                             remote_side=[id])

    def __repr__(self):
        return '{} {}'.format(self.code, self.title)


class Voucher(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_vouchers'

    index = db.Column(sa.Integer())
    date = db.Column(sa.Date(), default=datetime.datetime.today())

    creator_id = db.reference_col('bkr_users')
    creator = db.relationship('User', backref='vouchers')

    company_id = db.reference_col('bkr_companies')
    company = db.relationship('Company', backref='vouchers')

    period_id = db.reference_col('bkr_periods')
    period = db.relationship('Period', backref='vouchers')


class Record(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_records'

    summary = db.Column(sa.Unicode())
    direction = db.Column(ChoiceType(Direction, sa.SmallInteger()),
                          nullable=False, default=Direction.debit)
    amount = db.Column(sa.Numeric(16, 2), nullable=False)

    voucher_id = db.reference_col('bkr_vouchers')
    voucher = db.relationship('Voucher', backref='records')

    account_id = db.reference_col('bkr_accounts')
    account = db.relationship('Account', backref='records')
