# -*- coding: utf-8 -*-

from os.path import abspath, join, dirname, exists
from flask import redirect, flash, request, url_for, abort
from flask.templating import render_template
from flask.views import MethodView
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
from jinja2 import TemplateNotFound
from flask import current_app
from .models import User, Anonymous
from .extensions import login_manager


class BaseController(MethodView):

    template = 'base.html'
    header = ''
    title = ''
    breadcrumbs_prefix = [(u'Главная', 'index.page', {})]
    breadcrumbs = []
    sidebar_path = None
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def dispatch_request(self, **extra):
        return super(BaseController, self).dispatch_request(**extra)

    def get(self, **extra):
        return self.render(**extra)

    def post(self, **extra):
        return self.render(**extra)

    def redirect(self, location=None):
        if location is None:
            location = url_for("index.page")
        return redirect(location)

    def render(self, **extra):
        if current_user.is_authenticated() and not current_user.is_active() and request.endpoint != 'index.blocked':
            flash(_(u'Ваш аккаунт заблокирован'), 'error')
            return self.redirect(url_for('index.blocked'))
        title = self.title
        if not title:
            title = self.header
        if extra.get('template', False):
            self.template = extra.get('template', self.template)
        role = extra.get('role', current_user.get_role())
        if role:
            role = '_' + role
        """check templates/_ROLE/PATH
        after check templates/PATH"""
        if exists(abspath(join(dirname(abspath(__file__)), current_app.template_folder, role, self.template))):
            self.template = role + '/' + self.template
        # elif exists(abspath(join(dirname(abspath(__file__)), current_app.template_folder, self.template))):
        #     self.template = self.template
        if self.sidebar_path and exists(abspath(join(dirname(abspath(__file__)), current_app.template_folder, role, self.sidebar_path))):
            self.sidebar_path = role + '/' + self.sidebar_path
        breadcrumbs = []
        if self.breadcrumbs:
            breadcrumbs = self.breadcrumbs_prefix + self.breadcrumbs
        try:
            return render_template(self.template, header=self.header, title=title, breadcrumbs=breadcrumbs, sidebar_path=self.sidebar_path, **extra)
        except TemplateNotFound, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                abort(404)

    def sortable(self, q, model, field=None, default='', direction='asc'):
        for column in q.column_descriptions:
            if type(column['type']) == type(model):
                if model.__table__.name + '.' + field in [m.key for m in model.__table__.columns]:
                    return field, getattr(getattr(model, str(field)), direction)()
            elif field == column['name']:
                return (field, '%s %s' % (field, direction))
        return (default, ('%s.%s %s' % (model.__table__.name, default, direction)))
