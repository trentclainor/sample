# -*- coding: utf-8 -*-

from jinja2 import Markup, escape
from helpers import AppFactory
from settings import BaseConfig as Config
from session import RedisSessionInterface
from flask.ext.principal import RoleNeed, Identity, identity_loaded
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
from flask import url_for, request
from .extensions import principal, login_manager
from .models import User, Anonymous


app = AppFactory(Config).get_app(__name__, static_folder='static', template_folder='templates')
app.session_interface = RedisSessionInterface()

principals = principal(app)


def url_for_page(page):
    args = request.view_args.copy()
    args['page'] = page
    url_params = '&'.join(k + '=' + request.args[k] for k in reversed(list(request.args)))
    url_params = '?' + url_params if url_params else url_params
    return url_for(request.endpoint, **args) + url_params
app.jinja_env.globals['url_for_page'] = url_for_page


def url_for_next(endpoint, *args, **kwargs):
    args = request.view_args.copy()
    url_params = '&'.join(k + '=' + request.args[k] for k in reversed(list(request.args)))
    url_params = '?' + url_params if url_params else url_params
    kwargs['next'] = url_for(request.endpoint, **args) + url_params
    return url_for(endpoint, **kwargs)
app.jinja_env.globals['url_for_next'] = url_for_next


def url_for_sort(sort, direction):
    args = request.view_args.copy()
    for k in reversed(list(request.args)):
        args[k] = request.args[k]
    args['sort'] = sort
    if args.get('dir', direction) == 'asc':
        args['dir'] = 'desc'
    else:
        args['dir'] = 'asc'
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_sort'] = url_for_sort


@app.template_filter('nl2br')
def nl2br(string):
    return Markup('<br>'.join(escape(string).splitlines()))


@app.template_filter('num')
def num(string):
    if not string:
        string = 0
    return "{:,d}".format(int(string))


@app.template_filter('money')
def money(string):
    if not string:
        string = 0.0
    string = "%0.2f" % (float(string) / 100.0)
    return string + _(u' руб.')


@app.template_filter('unsafe')
def unsafe(string):
    return Markup(string).unescape()


@principals.identity_loader
def load_identity_when_session_expires():
    if hasattr(current_user, 'id'):
        return Identity(current_user.get_id())


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'get_role'):
        identity.provides.add(RoleNeed(current_user.get_role()))


@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    return user


def log_response(sender, response, **extra):
    sender.logger.debug('Request context is about to close down. Response: %s', response)


login_manager.login_view = 'account.signin'
login_manager.login_message = _(u'Авторизирутесь, чтобы продолжить')
login_manager.anonymous_user = Anonymous
