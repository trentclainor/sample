# -*- coding: utf-8 -*-

import os
from math import ceil
from flask import Flask, current_app, session
from string import ascii_letters, digits
from random import choice
from urlparse import urlparse, urljoin
from flask.ext.login import login_user as _login_user, logout_user as _logout_user
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed
from . import exception


class AppFactory(object):

    def __init__(self, config, envvar='PROJECT_SETTINGS', bind_db_object=True):
        self.app_config = config
        self.app_envvar = os.environ.get(envvar, False)
        self.bind_db_object = bind_db_object

    def get_app(self, app_module_name, **kwargs):
        self.app = Flask(app_module_name, **kwargs)
        self.app.config.from_object(self.app_config)
        self.app.config.from_envvar(self.app_envvar, silent=True)

        self._bind_extensions()
        self._register_blueprints()
        self._register_context_processors()

        return self.app

    def _get_imported_stuff_by_path(self, path):
        path = path.split('.')
        module_name = '.'.join(path[:-1])
        object_name = path[-1]
        module = __import__(module_name, fromlist=[object_name])
        return module, object_name

    def _bind_extensions(self):
        for ext_path in self.app.config.get('EXTENSIONS', []):
            module, e_name = self._get_imported_stuff_by_path(ext_path)
            if not hasattr(module, e_name):
                raise exception.NoExtension('No {e_name} extension found'.format(e_name=e_name))
            ext = getattr(module, e_name)
            if getattr(ext, 'init_app', False):
                ext.init_app(self.app)
            else:
                ext(self.app)

    def _register_context_processors(self):
        for processor_path in self.app.config.get('CONTEXT_PROCESSORS', []):
            module, p_name = self._get_imported_stuff_by_path(processor_path)
            if hasattr(module, p_name):
                self.app.context_processor(getattr(module, p_name))
            else:
                raise exception.NoContextProcessor('No {cp_name} context processor found'.format(cp_name=p_name))

    def _find_modules(self, blueprint_dir):
        from os import path, listdir
        dir = path.join(blueprint_dir + '/')
        try:
            return [blueprint_dir + '.' + f + '.module' for f in listdir(dir)
                if f.isalnum() and path.exists(blueprint_dir + '/' + f + '/__init__.py')]
        except OSError:
            return []

    def _register_blueprints(self):
        blueprints = self._find_modules(self.app.config.get('BLUEPRINTS_DIR'))
        for blueprint_path in blueprints:
            module, b_name = self._get_imported_stuff_by_path(blueprint_path)
            if hasattr(module, b_name):
                self.app.register_blueprint(getattr(module, b_name))
            else:
                raise exception.NoBlueprint('No {bp_name} blueprint found'.format(bp_name=b_name))


class Pagination(object):

    def __init__(self, query, page, per_page):
        self.page = page
        self.per_page = per_page
        self.items = query.limit(per_page).offset((page - 1) * per_page).all()
        if page == 1 and len(self.items) < per_page:
            self.total = len(self.items)
        else:
            self.total = query.order_by(None).count()

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def generate_random():
    return ''.join(choice(ascii_letters + digits) for n in xrange(40))


def is_safe_url(target, request):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target(request):
    for target in request.args.get('next'), request.path:
        if not target:
            continue
        if is_safe_url(target, request):
            return target


def login_user(user, remember=True):
    login = _login_user(user, remember)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.get_id()))
    return login


def logout_user():
    for key in ('identity.name', 'identity.auth_type', 'csrf', '_id'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return _logout_user()
