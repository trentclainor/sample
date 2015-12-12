# -*- coding: utf-8 -*-
from flask import url_for, request, flash, current_app, jsonify
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..controller import BaseController
from ..extensions import db
from ..decorators import roles_accepted
from ..helpers import Pagination
from ..models import User, CodeTemplate, Parameter, Section, Scenario, Channel
from ..users.views import UsersView, UserCreateView, UserEditView, UserPasswordEditView, UserDeleteView, UserBlockView, UserActivateView
from .forms import *
from . import preferences
from ..dictionary import *

STATUSES_BLOCKED = [k[0] for k in STATUSES_BLOCKED]
ADMIN_ROLES = [k[0] for k in ADMIN_ROLES]


class PreferencesView(BaseController):

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        if current_user.is_admin():
            return self.redirect(url_for('.managers'))
        else:
            return self.redirect(url_for('account.settings'))


class AdminsView(UsersView):
    template = 'preferences/users.html'
    sidebar_path = "helpers/preferences_sidebar.html"
    header = _(u'Администраторы')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Администраторы'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        return super(AdminsView, self).get(**extra)

    @roles_accepted('admin')
    def post(self, **extra):
        return super(AdminsView, self).post(**extra)


class AdminCreateView(UserCreateView):
    role = 'manager'
    form = UserAdminCreateForm
    header = _(u'Добавление администратора')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Администраторы'), 'preferences.managers', {}), (_(u'Добавление администратора'), '', {})]
    _messages = {
        'success': _(u'Администратор успешно добавлен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        return super(AdminCreateView, self).get(**extra)

    @roles_accepted('admin')
    def post(self, **extra):
        self.redirect_url = url_for("preferences.managers")
        return super(AdminCreateView, self).post(**extra)


class AdminEditView(UserEditView):
    role = 'manager'
    sidebar_path = "helpers/preferences_sidebar.html"
    form = UserAdminEditForm
    header = _(u'Редактирование администратора')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Администраторы'), 'preferences.managers', {}), (_(u'Редактирование администратора'), '', {})]
    _messages = {
        'success': _(u'Администратор успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        return super(AdminEditView, self).get(**extra)

    @roles_accepted('admin')
    def post(self, **extra):
        self.redirect_url = url_for("preferences.managers")
        return super(AdminEditView, self).post(**extra)


class AdminPasswordEditView(UserPasswordEditView):
    header = _(u'Смена пароля у администратора')
    sidebar_path = "helpers/preferences_sidebar.html"
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Администраторы'), 'preferences.managers', {}), (_(u'Смена пароля'), '', {})]
    _messages = {
        'success': _(u'Пароль успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        return super(AdminPasswordEditView, self).get(**extra)

    @roles_accepted('admin')
    def post(self, **extra):
        self.redirect_url = url_for("preferences.managers")
        return super(AdminPasswordEditView, self).post(**extra)


class AdminDeleteView(UserDeleteView):
    _messages = {
        'success': _(u'Администратор успешно удален'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for("preferences.managers")
        return super(AdminDeleteView, self).get(**extra)


class AdminBlockView(UserBlockView):
    _messages = {
        'success': _(u'Администратор успешно заблокирован'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for("preferences.managers")
        return super(AdminBlockView, self).get(**extra)


class AdminActivateView(UserActivateView):
    _messages = {
        'success': _(u'Администратор успешно активирован'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for("preferences.managers")
        return super(AdminActivateView, self).get(**extra)


class CodeTemplatesView(BaseController):
    sidebar_path = "helpers/preferences_sidebar.html"
    template = 'preferences/code_templates.html'
    header = _(u'Шаблоны')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Шаблоны'), '', {})]

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = FilterForm(request.args, csrf_enabled=False)
        query = form.query.data
        q = CodeTemplate.query.order_by(CodeTemplate.name)
        if query:
            q = q.filter(db.or_(
                CodeTemplate.name.like('%' + query + '%'),
                CodeTemplate.template.like('%' + query + '%'),
                CodeTemplate.template_static.like('%' + query + '%'),
            ))
        code_templates = q.paginate(extra.get('page', 1), CodeTemplate.per_page, False)
        return super(CodeTemplatesView, self).get(form=form, code_templates=code_templates, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        return super(CodeTemplatesView, self).post(*args, **extra)


class CodeTemplateCreateView(BaseController):
    header = _(u'Добавление шаблона')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Шаблоны'), 'preferences.code_templates', {}), (_(u'Добавление шаблона'), '', {})]
    sidebar_path = "helpers/preferences_sidebar.html"
    _messages = {
        'success': _(u'Шаблон успешно добален'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(CodeTemplateCreateView, self).get(form=CodeTemplateCreateForm(), **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        form = CodeTemplateCreateForm(request.form)
        if form.validate_on_submit():
            try:
                code_template = CodeTemplate(
                    name=form.name.data,
                    template=form.template.data,
                    template_static=form.template_static.data,
                )
                db.session.add(code_template)
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("preferences.code_templates")))
            except Exception, e:
                flash(self._messages['success'], 'success')
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(CodeTemplateCreateView, self).post(form=form, **extra)


class CodeTemplateEditView(BaseController):
    header = _(u'Редактирование шаблона')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Шаблоны'), 'preferences.code_templates', {}), (_(u'Редактирование шаблона'), '', {})]
    sidebar_path = "helpers/preferences_sidebar.html"
    _messages = {
        'success': _(u'Шаблон успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        code_template = CodeTemplate.query.get_or_404(extra.get('id'))
        form = CodeTemplateEditForm(obj=code_template)
        form.populate_obj(code_template)
        return super(CodeTemplateEditView, self).get(form=form, header_extend=code_template.name, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        code_template = CodeTemplate.query.get_or_404(extra.get('id'))
        form = CodeTemplateEditForm(request.form, obj=code_template)
        if form.validate_on_submit():
            form.populate_obj(code_template)
            try:
                result = code_template.update(
                    name=form.name.data,
                    template=form.template.data,
                    template_static=form.template_static.data,
                )
                if not result:
                    raise Exception('not save')
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("preferences.code_templates")))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(CodeTemplateEditView, self).post(form=form, **extra)


class CodeTemplateDeleteView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            code_template = CodeTemplate.query.get_or_404(extra.get('id'))
            code_template.delete()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ParametersView(BaseController):
    template = 'preferences/parameters.html'
    header = _(u'Параметры')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Параметры'), '', {})]
    sidebar_path = "helpers/preferences_sidebar.html"

    def dispatch_request(self, **extra):
        self.sidebar_path = "helpers/preferences_sidebar.html"
        return super(ParametersView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = FilterForm(request.args, csrf_enabled=False)
        query = form.query.data
        q = Parameter.query.order_by(Parameter.name)
        if query:
            q = q.filter(db.or_(
                Parameter.name.like('%' + query + '%'),
                Parameter.key.like('%' + query + '%'),
                Parameter.value.like('%' + query + '%'),
            ))
        parameters = q.paginate(extra.get('page', 1), Parameter.per_page, False)
        return super(ParametersView, self).get(form=form, parameters=parameters, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        return super(ParametersView, self).post(*args, **extra)


class ParameterCreateView(BaseController):
    header = _(u'Добавление параметра')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Параметры'), 'preferences.parameters', {}), (_(u'Добавление параметра'), '', {})]
    sidebar_path = "helpers/preferences_sidebar.html"
    _messages = {
        'success': _(u'Шаблон успешно добален'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def dispatch_request(self, **extra):
        self.sidebar_path = "helpers/preferences_sidebar.html"
        return super(ParameterCreateView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ParameterCreateView, self).get(form=ParameterCreateForm(), **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        form = ParameterCreateForm(request.form)
        if form.validate_on_submit():
            try:
                parameter = Parameter(
                    name=form.name.data,
                    key=form.key.data,
                    value=form.value.data,
                )
                parameter.save()
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("preferences.parameters")))
            except Exception, e:
                flash(self._messages['success'], 'success')
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(ParameterCreateView, self).post(form=form, **extra)


class ParameterEditView(BaseController):
    header = _(u'Редактирование параметра')
    breadcrumbs = [(_(u'Настройки'), 'preferences.index', {}), (_(u'Параметры'), 'preferences.parameters', {}), (_(u'Редактирование параметра'), '', {})]
    sidebar_path = "helpers/preferences_sidebar.html"
    _messages = {
        'success': _(u'Шаблон успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        parameter = Parameter.query.get_or_404(extra.get('id'))
        form = ParameterEditForm(obj=parameter)
        form.populate_obj(parameter)
        return super(ParameterEditView, self).get(form=form, header_extend=parameter.name, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        parameter = Parameter.query.get_or_404(extra.get('id'))
        form = ParameterEditForm(request.form, obj=parameter)
        if form.validate_on_submit():
            form.populate_obj(parameter)
            try:
                result = parameter.update(
                    name=form.name.data,
                    key=form.key.data,
                    value=form.value.data,
                )
                if not result:
                    raise Exception('not save')
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("preferences.parameters")))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(ParameterEditView, self).post(form=form, **extra)


class ParameterDeleteView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            parameter = Parameter.query.get_or_404(extra.get('id'))
            parameter.delete()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})

managers_view = AdminsView.as_view('managers')
code_templates_view = CodeTemplatesView.as_view('code_templates')
parameters_view = ParametersView.as_view('parameters')

preferences.add_url_rule('/', view_func=PreferencesView.as_view('index'))

preferences.add_url_rule('/managers/', defaults={'page': 1}, view_func=managers_view)
preferences.add_url_rule('/managers/<int:page>/', view_func=managers_view)
preferences.add_url_rule('/managers/create/', view_func=AdminCreateView.as_view('managers.create'))
preferences.add_url_rule('/managers/edit/<int:id>/', view_func=AdminEditView.as_view('managers.edit'))
preferences.add_url_rule('/managers/delete/<int:id>/', view_func=AdminDeleteView.as_view('managers.delete'))
preferences.add_url_rule('/managers/block/<int:id>/', view_func=AdminBlockView.as_view('managers.block'))
preferences.add_url_rule('/managers/activate/<int:id>/', view_func=AdminActivateView.as_view('managers.activate'))
preferences.add_url_rule('/managers/password/edit/<int:id>/', view_func=AdminPasswordEditView.as_view('managers.password.edit'))

preferences.add_url_rule('/code_templates/', defaults={'page': 1}, view_func=code_templates_view)
preferences.add_url_rule('/code_templates/<int:page>/', view_func=code_templates_view)
preferences.add_url_rule('/code_templates/create/', view_func=CodeTemplateCreateView.as_view('code_templates.create'))
preferences.add_url_rule('/code_templates/edit/<int:id>/', view_func=CodeTemplateEditView.as_view('code_templates.edit'))
preferences.add_url_rule('/code_templates/delete/<int:id>/', view_func=CodeTemplateDeleteView.as_view('code_templates.delete'))

preferences.add_url_rule('/parameters/', defaults={'page': 1}, view_func=parameters_view)
preferences.add_url_rule('/parameters/<int:page>/', view_func=parameters_view)
preferences.add_url_rule('/parameters/create/', view_func=ParameterCreateView.as_view('parameters.create'))
preferences.add_url_rule('/parameters/edit/<int:id>/', view_func=ParameterEditView.as_view('parameters.edit'))
preferences.add_url_rule('/parameters/delete/<int:id>/', view_func=ParameterDeleteView.as_view('parameters.delete'))
