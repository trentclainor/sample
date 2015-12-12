# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _


class Auth(Exception):
    pass


class AccessDenied(Exception):

    def __str__(self):
        return 'Access Denied'

    def __unicode__(self):
        return _(u'Доступ запрещен')


class NoContextProcessor(Exception):
    pass


class NoBlueprint(Exception):
    pass


class NoExtension(Exception):
    pass


class FeedbackCreate(Exception):
    pass


class UserCreate(Exception):
    pass
