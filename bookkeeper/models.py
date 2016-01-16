import datetime
from enum import IntEnum

import sqlalchemy as sa
from decent.web import db
from decent.web.cache import cache
from flask import session
from flask.ext.principal import Permission
from flask.ext.security import RoleMixin, UserMixin
from sqlalchemy import event
from sqlalchemy_utils import ChoiceType

from . import const


class Direction(IntEnum):
    debit = 1
    credit = -1

    def __str__(self):
        return self.label


Direction.debit.label = '借'
Direction.credit.label = '贷'


class CompanyRole(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_company_roles'

    user_id = db.reference_col('bkr_users')
    user = db.relationship('User', backref='company_roles')

    company_id = db.reference_col('bkr_companies')
    company = db.relationship('Company', backref='roles')

    role_id = db.reference_col('bkr_roles')
    role = db.relationship('Role')

    @property
    def perm(self):
        return const.P_COMPANY_ROLE(self.company_id, self.role_cached.name)

    @property
    def role_cached(self):
        return Role.get_by_id(self.role_id)


class User(db.Model, db.SurrogatePK, UserMixin):
    __tablename__ = 'bkr_users'

    email = db.Column(sa.Unicode(), unique=True)
    password = db.Column(sa.Unicode())
    active = db.Column(sa.Boolean())
    confirmed_at = db.Column(sa.DateTime())
    last_login_at = db.Column(sa.DateTime())
    current_login_at = db.Column(sa.DateTime())
    last_login_ip = db.Column(sa.Unicode())
    current_login_ip = db.Column(sa.Unicode())
    login_count = db.Column(sa.BigInteger())

    def __str__(self):
        return self.email or str(self.id)

    # @cache.memoize()
    def all_needs(self):
        def gen():
            if self.active:
                yield const.P_USER_ACTIVE
            for role in self.get_roles():
                yield role.perm
                yield const.P_COMPANY(role.company_id)

        return list(gen())

    @property
    def current_company(self):
        rv = None
        company_id = session.get('CURRENT_COMPANY')
        if company_id:
            rv = Company.get_by_id(company_id)
        roles = self.get_roles()
        if rv:
            for role in roles:
                if rv.id == role.company_id:
                    break
            else:
                rv = None
        if not rv and roles:
            rv = roles[0].company
            session['CURRENT_COMPANY'] = rv.id
        return rv

    @current_company.setter
    def current_company(self, val):
        id_ = getattr(val, 'id', val)
        with Permission(
                const.P_SUPER_ADMIN,
                const.P_COMPANY(id_),
        ).require(http_exception=403):
            session['CURRENT_COMPANY'] = id_
            cache.delete_memoized(self.get_roles_cached)

    @property
    def current_period(self):
        rv = None
        period_id = session.get('CURRENT_PERIOD')
        if period_id:
            rv = Period.get_by_id(period_id)
        if not rv:
            now = datetime.datetime.today()
            rv = Period.query.filter_by(year=now.year, month=now.month).one()
            if not rv:
                rv = Period.create(year=now.year, month=now.month)
            session['CURRENT_PERIOD'] = rv.id
        return rv

    @current_period.setter
    def current_period(self, val):
        session['CURRENT_PERIOD'] = getattr(val, 'id', val)

    @property
    def roles(self):
        company = self.current_company
        if company:
            rv = [r.role_cached for r in self.get_roles()
                  if r.company.id == company.id or
                  r.role_cached.name == const.P_SUPER_ADMIN[-1]]
            return rv
        else:
            return []

    def get_roles(self):
        roles = self.get_roles_cached()
        rv = []
        for role in roles:
            if role in db.db.session:
                rv.append(role)
            else:
                rv.append(db.db.session.merge(role, load=False))
        return rv

    @cache.memoize()
    def get_roles_cached(self):
        return self.company_roles


# @event.listens_for(User.active, 'set')
# def on_user_active_change(target, *_):
#     db.db.session.delete_memoized(target.all_needs)


@event.listens_for(CompanyRole, 'after_insert')
@event.listens_for(CompanyRole, 'after_update')
@event.listens_for(CompanyRole, 'after_delete')
def on_user_roles_change(mapper, conn, target):
    # noinspection PyArgumentList
    stub = User(id=target.user_id)
    db.db.session.delete_memoized(stub.get_roles_cached)


class Role(db.Model, db.SurrogatePK, RoleMixin):
    __tablename__ = 'bkr_roles'

    name = db.Column(sa.Unicode(), unique=True)
    description = db.Column(sa.Unicode())

    def __str__(self):
        return self.description or ''

    @classmethod
    def get_by_need(cls, need):
        return cls.query.filter_by(name=need[-1]).one()


class Company(db.Model, db.SurrogatePK):
    __tablename__ = 'bkr_companies'

    name = db.Column(sa.Unicode())

    def __str__(self):
        return self.name or ''

    @property
    def perm(self):
        return const.P_COMPANY(self.id)


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
