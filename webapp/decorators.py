# -*- coding: utf-8 -*-
from flask import redirect, url_for, flash
# from helpers import logout_user
from functools import wraps
# from flask.ext.login import current_user, login_required
from flask.ext.principal import RoleNeed, Permission
from flask.ext.babel import gettext as _


# def roles_required(*roles):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             return fn(*args, **kwargs)
#         return decorated_view
#     return wrapper
#
#

def roles_accepted(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*[RoleNeed(role) for role in roles])
            if perm.can():
                return fn(*args, **kwargs)
            flash(_(u'Нет прав для просмотра этой страницы'), 'info')
            # logout_user()
            # if not current_user.is_authenticated():
            #     return current_app.login_manager.unauthorized()
            # return fn(*args, **kwargs)
            return redirect(url_for('index.page'))
        return decorated_view
    return wrapper
