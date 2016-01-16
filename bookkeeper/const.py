from functools import partial

from flask.ext.principal import RoleNeed, TypeNeed, ItemNeed

P_SUPER_ADMIN = RoleNeed('super')
P_ADMIN = RoleNeed('admin')
P_USER_ACTIVE = TypeNeed('active')
P_COMPANY_ROLE = partial(ItemNeed, 'company')
P_COMPANY = partial(P_COMPANY_ROLE, type='_in')
P_COMPANY_ADMIN = partial(P_COMPANY_ROLE, type='admin')
