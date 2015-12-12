# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _


class BaseConfig(object):

    EXTENSIONS = [
        'webapp.extensions.db',
        'webapp.extensions.login_manager',
        'webapp.extensions.gravatar',
        'webapp.extensions.toolbar',
        'webapp.extensions.mail',
        'webapp.extensions.babel',
        'webapp.extensions.principal',
        'webapp.extensions.csrf',
    ]

    CONTEXT_PROCESSORS = [
        'webapp.context_processors.common',
    ]

    BLUEPRINTS_DIR = 'webapp'

    ROLE = [
        ('client', _(u'Клиент')),
        ('partner', _(u'Партнер')),
    ]

    DATE_FORMAT = '%d.%m.%Y'
    DATE_TO_FORMAT = '%d.%m.%Y %H:%M:%S'
    DATE_FROM_FORMAT = '%d.%m.%Y %H:%M:%S'

    CACHE = ['127.0.0.1:11211']
    SQLALCHEMY_DATABASE_URI = 'postgresql://sample:sample@localhost/sample'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'asaats0919191,442$22004484$$@99}}aD()'
    SESSION_COOKIE_NAME = 'sid'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG = False
    TESTING = False

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'Xasaets0919191,442$22004484$$@99}}()'

    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6Lc-k_ASAAAAAInWbZJzJARIhLBEFreoKWHWZ9dH'
    RECAPTCHA_PRIVATE_KEY = '6Lc-k_ASAAAAAId7AtuQPqOcY3jMs75bZZDaTP1r'

    MAIL_MAILER = '/usr/sbin/sendmail'
    MAIL_MAILER_FLAGS = '-t'
    DEFAULT_MAIL_SENDER = _(u'Sample Robot <support@localhost>')
    MAIL_DEFAULT_SENDER = _(u'Sample Robot <support@localhost>')
    DEFAULT_MAX_EMAILS = None
    MAIL_FAIL_SILENTLY = False
    MAIL_SUPPRESS_SEND = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
