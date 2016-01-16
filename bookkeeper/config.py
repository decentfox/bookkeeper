SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bkr'

SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True

MAIL_SERVER = ''
MAIL_PORT = 994
MAIL_USE_SSL = True
SECURITY_EMAIL_SENDER = MAIL_USERNAME = ''
MAIL_PASSWORD = ''

try:
    from .local_config import *
except ImportError:
    pass
