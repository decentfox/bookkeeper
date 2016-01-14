import datetime
from enum import IntEnum

import sqlalchemy as sa
from decent.web import db
from decent.web.cache import cache
from flask import session
from flask.ext.principal import ItemNeed, Permission
from flask.ext.security import RoleMixin, UserMixin
from sqlalchemy import event
from sqlalchemy_utils import ChoiceType


class Direction(IntEnum):
    debit = 1
    credit = -1

    def __str__(self):
        return self.label


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
    r_roles = db.relationship('Role', secondary=roles_x_users, backref='users')

    def __str__(self):
        return self.email or str(self.id)

    @cache.memoize()
    def all_needs(self):
        def gen():
            for company in self.companies:
                yield company.perm

        return list(gen())

    @property
    def current_company(self):
        rv = None
        company_id = session.get('CURRENT_COMPANY')
        if company_id:
            rv = Company.get_by_id(company_id)
            if not Permission(rv.perm).can():
                session.pop('CURRENT_COMPANY')
                rv = None
        if not rv and self.companies:
            rv = self.companies[0]
            session['CURRENT_COMPANY'] = rv.id
        return rv

    @current_company.setter
    def current_company(self, val):
        session['CURRENT_COMPANY'] = getattr(val, 'id', val)

    @property
    def roles(self):
        return self.get_roles()

    @cache.memoize()
    def get_roles(self):
        return self.r_roles


@event.listens_for(User.companies, 'dispose_collection')
def on_user_companies_change(target, *_):
    db.db.session.delete_memoized(target.all_needs)


@event.listens_for(User.r_roles, 'dispose_collection')
def on_user_roles_change(target, *_):
    db.db.session.delete_memoized(target.get_roles)


class Role(db.Model, db.SurrogatePK, RoleMixin):
    __tablename__ = 'bkr_roles'

    name = db.Column(sa.Unicode(), unique=True)
    description = db.Column(sa.Unicode())

    def __str__(self):
        return self.description or ''


class Company(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_companies'

    name = db.Column(sa.Unicode())

    def __str__(self):
        return self.name or ''

    @property
    def perm(self):
        return ItemNeed('in', self.id, self.__tablename__)


class Period(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_periods'

    year = db.Column(sa.Integer())
    month = db.Column(sa.SmallInteger())

    def __str__(self):
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

    def __str__(self):
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
