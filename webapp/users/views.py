# -*- coding: utf-8 -*-
from flask import url_for, request, flash, current_app, jsonify
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..controller import BaseController
from ..extensions import db
from ..decorators import roles_accepted
from ..helpers import Pagination
from ..models import User, CodeTemplate, Parameter, Section, Scenario, Channel, Link, ReportScenario
from .forms import *
from ..dictionary import *

STATUSES_BLOCKED = [k[0] for k in STATUSES_BLOCKED]
ADMIN_ROLES = [k[0] for k in ADMIN_ROLES]


class UsersView(BaseController):
    role = None

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = UserFilterForm(request.args, csrf_enabled=False)
        sort = request.args.get('sort', 'id')
        direction = request.args.get('dir', 'asc')
        status = form.status.data
        query = form.query.data
        channel_alias = db.aliased(Channel)
        if self.role == 'client':
            q = db.engine.execute('select id,name from users as u')
            q = User.query.with_entities(
                User,
                db.func.count(db.func.distinct(channel_alias.id)).label("channels"),
                db.func.count(db.func.distinct(channel_alias.partner_id)).label("partners"),
            )\
            .filter(User.role == self.role)\
            .outerjoin(Section, db.and_(Section.client_id == User.id, Section.status == 'active'))\
            .outerjoin(Scenario, db.and_(Scenario.client_id == User.id, Scenario.status == 'active'))\
            .outerjoin(Channel, db.and_(User.id == Channel.partner_id, Channel.status == 'active'))\
            .outerjoin(Link, Link.scenario_id == Scenario.id)\
            .outerjoin(channel_alias, db.and_(Link.channel_id == channel_alias.id, channel_alias.status == 'active'))\
            .group_by(User.id)
        elif self.role == 'partner':
            q = User.query.with_entities(
                User,
                db.func.count(db.func.distinct(Channel.id)).label("channels"),
                db.func.count(db.func.distinct(Scenario.client_id)).label("clients"),
            )\
            .filter(User.role == self.role)\
            .outerjoin(Channel, db.and_(User.id == Channel.partner_id, Channel.status == 'active'))\
            .outerjoin(Link, Link.channel_id == Channel.id)\
            .outerjoin(Scenario, db.and_(Scenario.id == Link.scenario_id, Scenario.status == 'active'))\
            .group_by(User.id)
        elif current_user.is_admin():
            q = User.query.filter(User.role.in_(ADMIN_ROLES))
        if status == 'end_money':
            q = q.filter(User.money == 0)
        elif status:
            q = q.filter(User.status == status)
        if not current_user.is_admin():
            q = q.filter(User.status.in_(STATUSES_BLOCKED))
        if query:
            q = q.filter(db.or_(
                User.name.like('%' + query + '%'),
                User.email.like('%' + query + '%'),
                User.company.like('%' + query + '%'),
                User.contact_name.like('%' + query + '%'),
                User.phone.like('%' + query + '%'),
                User.address.like('%' + query + '%'),
                User.comment.like('%' + query + '%'),
            ))
            # .outerjoin(Link, db.and_(Scenario.id == Link.scenario_id, Channel.id == Link.channel_id, Link.status == 'active'))\
        sort, column_sorted = self.sortable(q, User, field=sort, default='name', direction=direction)
        q = q.order_by(column_sorted)
        users = Pagination(q, extra.get('page', 1), User.per_page)
        return super(UsersView, self).get(form=form, users=users, default_sort=sort, default_dir=direction, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, role=None, **extra):
        return super(UsersView, self).post(role=None, **extra)


class UserCreateView(BaseController):
    form = UserCreateForm
    role = None
    redirect_url = None

    def dispatch_request(self, **extra):
        if not self.redirect_url:
            self.redirect_url = url_for('preferences.index')
        return super(UserCreateView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(UserCreateView, self).get(form=self.form(), **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        form = self.form(request.form)
        if self.role == 'manager' and current_user.is_admin():
            self.role = form.role.data
        if form.validate_on_submit():
            try:
                user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password=form.passwd.data,
                    role=self.role,
                    company=form.company.data,
                    contact_name=form.contact_name.data,
                    phone=form.phone.data,
                    address=form.address.data,
                    comment=form.comment.data,
                )
                db.session.add(user)
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(self.redirect_url)
            except Exception, e:
                flash(self._messages['success'], 'success')
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(UserCreateView, self).post(form=form, **extra)


class UserEditView(BaseController):
    redirect_url = None
    form = UserEditForm

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        user = User.query.get_or_404(extra.get('id'))
        form = self.form(obj=user)
        form.populate_obj(user)
        return super(UserEditView, self).get(form=form, header_extend=user.name, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        user = User.query.get_or_404(extra.get('id'))
        form = self.form(request.form, obj=user)
        if current_user.is_admin():
            self.role = form.role.data
        if form.validate_on_submit():
            form.populate_obj(user)
            try:
                if form.passwd:
                    result = user.update(
                        name=form.name.data,
                        email=form.email.data,
                        password=form.passwd.data,
                        role=self.role,
                        company=form.company.data,
                        contact_name=form.contact_name.data,
                        phone=form.phone.data,
                        address=form.address.data,
                        comment=form.comment.data,
                    )
                else:
                    result = user.update(
                        name=form.name.data,
                        email=form.email.data,
                        role=self.role,
                        company=form.company.data,
                        contact_name=form.contact_name.data,
                        phone=form.phone.data,
                        address=form.address.data,
                        comment=form.comment.data,
                    )
                if not result:
                    raise Exception('not save')
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", self.redirect_url))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(UserEditView, self).post(form=form, **extra)


class UserPasswordEditView(BaseController):
    redirect_url = None
    form = UserPasswordEditForm
    header = _(u'Смена пароля')
    _messages = {
        'success': _(u'Пароль изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        user = User.query.get_or_404(extra.get('id'))
        form = self.form(obj=user)
        form.populate_obj(user)
        return super(UserPasswordEditView, self).get(form=form, header_extend=user.name, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        user = User.query.get_or_404(extra.get('id'))
        form = self.form(request.form, obj=user)
        if form.validate_on_submit():
            form.populate_obj(user)
            try:
                result = user.update(
                    password=form.passwd.data,
                )
                if not result:
                    raise Exception('not save')
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", self.redirect_url))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(UserPasswordEditView, self).post(form=form, **extra)


class UserDeleteView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            user = User.query.get_or_404(extra.get('id'))
            user.delete()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class UserBlockView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            user = User.query.get_or_404(extra.get('id'))
            user.block()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class UserActivateView(BaseController):
    redirect_url = None

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            user = User.query.get_or_404(extra.get('id'))
            user.activate()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})
