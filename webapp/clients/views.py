# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import url_for, request, flash, current_app, jsonify, abort
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from sqlalchemy.orm.exc import NoResultFound
from ..controller import BaseController
from ..extensions import db
from ..decorators import roles_accepted
from ..models import User, Scenario, Section, ScenarioSection, Channel, Link
from ..users.views import UsersView, UserCreateView, UserEditView, UserPasswordEditView, UserDeleteView, UserBlockView, UserActivateView
from ..stats.views import StatsDaysView, StatsScenariosView, StatsPartnersView, StatsChannelsView
from ..helpers import Pagination
from ..dictionary import *
from .forms import *
from . import clients

STATUSES_BLOCKED = [k[0] for k in STATUSES_BLOCKED]


class ClientsView(UsersView):
    role = 'client'
    template = 'clients.html'
    # sidebar_path = 'helpers/clients_sidebar.html'
    header = _(u'Клиенты')
    breadcrumbs = [(_(u'Клиенты'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ClientsView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        return super(ClientsView, self).post(**extra)


class ClientCreateView(UserCreateView):
    role = 'client'
    header = _(u'Добавление клиента')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Добавление клиента'), '', {})]
    _messages = {
        'success': _(u'Клиент успешно добавлен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ClientCreateView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        self.redirect_url = url_for('clients.index')
        return super(ClientCreateView, self).post(**extra)


class ClientEditView(UserEditView):
    role = 'client'
    header = _(u'Редактирование клиента')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Редактирование клиента'), '', {})]
    _messages = {
        'success': _(u'Клиент успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ClientEditView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        self.redirect_url = url_for('clients.index')
        return super(ClientEditView, self).post(**extra)


class ClientPasswordEditView(UserPasswordEditView):
    role = 'client'
    header = _(u'Смена пароля у клиента')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Смена пароля'), '', {})]
    _messages = {
        'success': _(u'Пароль успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ClientPasswordEditView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        self.redirect_url = url_for('clients.index')
        return super(ClientPasswordEditView, self).post(**extra)


class ClientDeleteView(UserDeleteView):
    _messages = {
        'success': _(u'Клиент успешно удален'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for('clients.index')
        return super(ClientDeleteView, self).get(**extra)


class ClientBlockView(UserBlockView):
    _messages = {
        'success': _(u'Клиент успешно заблокирован'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for('clients.index')
        return super(ClientBlockView, self).get(**extra)


class ClientActivateView(UserActivateView):
    _messages = {
        'success': _(u'Клиент успешно активирован'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for('clients.index')
        return super(ClientActivateView, self).get(**extra)


class ClientCodeView(BaseController):
    template = 'clients/code.html'
    header = _(u'Получение универсально кода')
    header_extend = ''
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Получение универсально кода'), '', {})]

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client = User.get_or_404(extra.get('id'))
        self.header_extend = _(u' для ') + client.name
        return super(ClientCodeView, self).dispatch_request(client=client, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        client = extra.get('client')
        form = ClientCodeForm(request.args, obj=client, csrf_enabled=False)
        return super(ClientCodeView, self).get(form=form, header_extend=self.header_extend, **extra)


class SectionsView(BaseController):
    template = 'clients/sections.html'
    header = _(u'Разделы')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Разделы'), '', {})]

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        if client_id:
            client = User.get_or_404(client_id)
            self.header += _(u' для ') + client.name
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Разделы для ') + client.name, '', '')
        return super(SectionsView, self).dispatch_request(scenario=request.args.get('scenario', 0), **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = SectionFilterForm(request.args, csrf_enabled=False, **extra)
        sort = request.args.get('sort', 'name')
        direction = request.args.get('dir', 'asc')
        status = None
        if form.status:
            status = form.status.data
        query = form.query.data
        client_id = extra.get('client_id', None)
        q = Section.query
        scenario_id = None
        if form.scenario:
            scenario_id = form.scenario.data
        if scenario_id:
            q = Section.query.with_entities(Section).join(
                    ScenarioSection,
                    db.and_(
                        ScenarioSection.scenario_id == scenario_id,
                        ScenarioSection.section_id == Section.id,
                    )).group_by(Section.id)
        if status:
            q = q.filter(Section.status == status)
        if client_id:
            q = q.filter(Section.client_id == client_id)

        sort, column_sorted = self.sortable(q, Section, field=sort, default='client_id, sections.order', direction=direction)
        q = q.order_by(column_sorted)
        if query:
            q = q.filter(db.or_(
                Section.name.like('%' + query + '%'),
                Section.alias.like('%' + query + '%'),
                Section.wildcard.like('%' + query + '%'),
            ))
        sections = q.paginate(extra.get('page', 1), Section.per_page, False)
        return super(SectionsView, self).get(form=form, default_sort=sort, default_dir=direction, sections=sections, **extra)


class SectionCreateView(BaseController):
    form = SectionCreateForm
    header = _(u'Добавление раздела')
    header_extend = ''
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Разделы'), 'clients.sections', {}), (_(u'Добавление раздела'), '', {})]
    _messages = {
        'success': _(u'Раздел успешно добавлен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id', None)
        if client_id:
            # self.form = SectionClientCreateForm
            client = User.get_or_404(client_id)
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Разделы для ') + client.name, 'clients.sections', {'client_id': client_id})
        return super(SectionCreateView, self).dispatch_request(client=client, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(SectionCreateView, self).get(form=self.form(request.args, **extra), header_extend=self.header_extend, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        client_id = extra.get('client_id')
        form = self.form(request.form, **extra)
        if form.validate_on_submit():
            try:
                max_order = Section.query.with_entities(db.func.max(Section.order).label("order")).filter(Section.client_id == client_id).one().order or 0
                section = Section(
                    client_id=client_id,
                    order=max_order + 1,
                    name=form.name.data,
                    alias=form.alias.data,
                    section_type=form.section_type.data,
                    wildcard=form.wildcard.data,
                )
                db.session.add(section)
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("clients.sections", client_id=client_id)))
            except Exception, e:
                flash(self._messages['success'], 'success')
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(SectionCreateView, self).post(form=form, **extra)


class SectionEditView(BaseController):
    header = _(u'Редактирование раздела')
    header_extend = ''
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Разделы'), 'clients.sections', {}), (_(u'Редактирование раздела'), '', {})]
    _messages = {
        'success': _(u'Раздел успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        section = Section.get_or_404(extra.get('id'))
        client = section.client
        self.header_extend = _(u'для ') + client.name
        self.breadcrumbs[1] = (_(u'Разделы для ') + client.name, 'clients.sections', {'client_id': section.client_id})
        return super(SectionEditView, self).dispatch_request(client_id=section.client_id, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        section = Section.get_or_404(extra.get('id'))
        form = SectionEditForm(obj=section)
        form.populate_obj(section)
        return super(SectionEditView, self).get(form=form, header_extend=self.header_extend, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        section = Section.query.get_or_404(extra.get('id'))
        form = SectionEditForm(request.form, obj=section)
        if form.validate_on_submit():
            form.populate_obj(section)
            try:
                result = section.update(
                    name=form.name.data,
                    alias=form.alias.data,
                    section_type=form.section_type.data,
                    wildcard=form.wildcard.data,
                )
                if not result:
                    raise Exception('not save')
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("clients.sections", client_id=section.client_id)))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(SectionEditView, self).post(form=form, header_extend=self.header_extend, **extra)


class SectionCodeView(BaseController):
    template = 'clients/section_code.html'
    header = _(u'Получение кода раздела')
    header_extend = ''
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Разделы'), 'clients.sections', {}), (_(u'Получение кода раздела'), '', {})]

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        section = Section.get_or_404(extra.get('id'))
        if section:
            client = section.client
            self.header_extend = section.name + _(u' для ') + client.name
            self.breadcrumbs[1] = (_(u'Разделы для ') + client.name, 'clients.sections', {'client_id': client.get_id()})
        return super(SectionCodeView, self).dispatch_request(section=section, client_id=client.get_id(), **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        section = extra.get('section')
        form = SectionCodeForm(request.args, obj=section, csrf_enabled=False)
        return super(SectionCodeView, self).get(form=form, header_extend=self.header_extend, **extra)


class SectionActivateView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            section = Section.query.get_or_404(extra.get('id'))
            section.activate()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class SectionDeleteView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            section = Section.query.get_or_404(extra.get('id'))
            section.delete()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class SectionUpView(BaseController):

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        try:
            current_section = Section.query.get_or_404(extra.get('id'))
            upper_section = Section.query.filter(Section.client_id == current_section.client_id, Section.order == current_section.order - 1).one()
            current_order = current_section.order
            upper_order = upper_section.order
            upper_section.update(order=current_order, commit=False)
            current_section.update(order=upper_order, commit=False)
            db.session.commit()
            return self.redirect(request.args.get("next", url_for("clients.sections", client_id=current_section.client_id)))
        except NoResultFound:
            db.session.rollback()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                flash(self._messages['internal_error'], 'error')
            db.session.rollback()
        return super(SectionUpView, self).post(**extra)


class SectionDownView(BaseController):

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        try:
            current_section = Section.query.get_or_404(extra.get('id'))
            downed_section = Section.query.filter(Section.client_id == current_section.client_id, Section.order == current_section.order + 1).one()
            current_order = current_section.order
            downed_order = downed_section.order
            downed_section.update(order=current_order, commit=False)
            current_section.update(order=downed_order, commit=False)
            db.session.commit()
            return self.redirect(request.args.get("next", url_for("clients.sections", client_id=current_section.client_id)))
        except NoResultFound:
            db.session.rollback()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                flash(self._messages['internal_error'], 'error')
            db.session.rollback()
        return super(SectionDownView, self).post(**extra)


class ScenariosView(BaseController):
    template = 'clients/scenarios.html'
    header = _(u'Сценарии')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Сценарии'), '', {})]

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id', None)
        if client_id:
            client = User.get_or_404(client_id)
            self.header += _(u' для ') + client.name
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Сценарии для ') + client.name, '', '')
        return super(ScenariosView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin', 'client')
    def get(self, **extra):
        form = ScenarioFilterForm(request.args, csrf_enabled=False)
        sort = request.args.get('sort', 'name')
        direction = request.args.get('dir', 'asc')
        client_id = extra.get('client_id', None)
        status = None
        if form.status:
            status = form.status.data
        query = form.query.data
        q = Scenario.query
        if status:
            q = q.filter(Scenario.status == status)
        if client_id:
            q = q.filter(Scenario.client_id == client_id)
        if not current_user.is_admin():
            q = q.filter(Scenario.status.in_(STATUSES_BLOCKED))
        sort, column_sorted = self.sortable(q, Scenario, field=sort, default='id', direction=direction)
        q = q.order_by(column_sorted)
        if query:
            q = q.filter(db.or_(
                Scenario.name.like('%' + query + '%'),
                Scenario.cost_type.like('%' + query + '%'),
                Scenario.moderation.like('%' + query + '%'),
            ))
        q = q.group_by(Scenario.id)
        scenarios = q.paginate(extra.get('page', 1), Scenario.per_page, False)
        return super(ScenariosView, self).get(form=form, default_sort=sort, default_dir=direction, scenarios=scenarios, **extra)


class ScenarioCreateView(BaseController):
    template = 'clients/scenario_create.html'
    form = ScenarioCreateForm
    header = _(u'Добавление сценария')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Сценарии'), 'clients.scenarios', {}), (_(u'Добавление сценария'), '', {})]
    _messages = {
        'success': _(u'Сценарий успешно добавлен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id', None)
        if client_id:
            client = User.get_or_404(client_id)
            self.header += _(u' для ') + client.name
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Сценарии для ') + client.name, 'clients.scenarios', {'client_id': client_id})
        return super(ScenarioCreateView, self).dispatch_request(client=client, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ScenarioCreateView, self).get(form=self.form(request.args, **extra), **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        form = self.form(request.form, **extra)
        if form.validate_on_submit():
            client_id = extra.get('client').get_id()
            try:
                count_unique = form.count_unique.data
                total_count = form.total_count.data
                section_scenarios = []
                checked = 0
                for section in form.section_list.data:
                    count = section.get('count')
                    if total_count > 0:
                        count = 0
                    if section.get('checked'):
                        checked += 1
                        section_scenarios.append((Section.query.filter(db.and_(Section.id == section.get('section_id'), Section.client_id == client_id)).first(), count))
                if count_unique and total_count > checked:
                    total_count = checked
                scenario = Scenario(
                    client_id=client_id,
                    name=form.name.data,
                    cost_type=form.cost_type.data,
                    price=form.price.data * 100,
                    moderation=form.moderation.data,
                    total_count=total_count,
                    count_unique=count_unique,
                )
                db.session.add(scenario)
                for section, count in section_scenarios:
                    scenario.scenario_sections.append(ScenarioSection(section, scenario, count))
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("clients.scenarios", client_id=client_id)))
            except Exception, e:
                flash(self._messages['success'], 'success')
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(ScenarioCreateView, self).post(form=form, **extra)


class ScenarioEditView(BaseController):
    template = 'clients/scenario_edit.html'
    header = _(u'Редактирование сценария')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), (_(u'Сценарии'), 'clients.scenarios', {}), (_(u'Редактирование сценария'), '', {})]
    _messages = {
        'success': _(u'Сценарий успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        scenario = Scenario.get_or_404(extra.get('id'))
        scenario.price = float(scenario.get_price())
        client = scenario.client
        self.header_extend = _(u'для ') + client.name
        self.breadcrumbs[1] = (_(u'Сценарии для ') + client.name, 'clients.scenarios', {'client_id': scenario.client_id})
        return super(ScenarioEditView, self).dispatch_request(scenario=scenario, client_id=scenario.client_id, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        scenario = extra.get('scenario')
        form = ScenarioEditForm(obj=scenario)
        # form.populate_obj(scenario)
        return super(ScenarioEditView, self).get(form=form, header_extend=scenario.name, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        scenario = extra.get('scenario')
        form = ScenarioEditForm(request.form, obj=scenario)
        if form.validate_on_submit():
            try:
                count_unique = form.count_unique.data
                total_count = form.total_count.data
                section_scenarios = []
                checked = 0
                for section in form.section_list.data:
                    count = section.get('count')
                    if total_count > 0:
                        count = 0
                    if section.get('checked'):
                        checked += 1
                        section_scenarios.append((Section.query.filter(db.and_(Section.id == section.get('section_id'), Section.client_id == scenario.client_id)).first(), count))
                if count_unique and total_count > checked:
                    total_count = checked
                result = scenario.update(
                    commit=False,
                    name=form.name.data,
                    cost_type=form.cost_type.data,
                    price=form.price.data * 100,
                    moderation=form.moderation.data,
                    total_count=form.total_count.data,
                    count_unique=form.count_unique.data,
                )
                scenario.scenario_sections = []
                for section, count in section_scenarios:
                    scenario.scenario_sections.append(ScenarioSection(section, scenario, count))
                if not result:
                    raise Exception('not save')
                flash(self._messages['success'], 'success')
                db.session.commit()
                return self.redirect(request.args.get("next", url_for("clients.scenarios", client_id=scenario.client_id)))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(ScenarioEditView, self).post(form=form, **extra)


class ScenarioActivateView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            scenario = Scenario.query.get_or_404(extra.get('id'))
            scenario.activate()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ScenarioBlockView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            scenario = Scenario.query.get_or_404(extra.get('id'))
            scenario.block()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ScenarioDeleteView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            scenario = Scenario.query.get_or_404(extra.get('id'))
            scenario.delete()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ChannelsView(BaseController):
    template = 'clients/channels.html'
    header = _(u'Каналы')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), ('', '', {})]
    _messages = {
        'success': _(u'Каналы успешно удалены'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        scenario = int(request.args.get('scenario', 0))
        client = User.get_or_404(client_id)
        self.header += _(u' для ') + client.name
        self.header_extend = _(u'для ') + client.name
        self.breadcrumbs[1] = (_(u'Каналы для ') + client.name, '', '')
        return super(ChannelsView, self).dispatch_request(scenario=scenario, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ChannelFilterForm(request.args, csrf_enabled=False, **extra)
        sort = request.args.get('sort', 'name')
        direction = request.args.get('dir', 'asc')
        status = None
        if form.status:
            status = form.status.data
        query = form.query.data
        client_id = extra.get('client_id', None)
        if form.scenario:
            scenario_id = form.scenario.data
        if scenario_id:
            q = Channel.query.with_entities(
                Channel,
                Link,
                )\
                .join(Link, db.and_(Link.channel_id == Channel.id, Link.scenario_id == scenario_id))\
                .join(Scenario, db.and_(Scenario.id == Link.scenario_id, Scenario.client_id == client_id))\
                .join(User, User.id == Scenario.client_id)\
                .group_by(Channel.id)
        else:
            q = Channel.query.with_entities(Channel,
            Link)\
                .join(Link, db.and_(Link.channel_id == Channel.id))\
                .join(Scenario, db.and_(Scenario.id == Link.scenario_id, Scenario.client_id == client_id))\
                .join(User, User.id == Scenario.client_id)\
                .group_by(Channel.id)
        if status:
            q = q.filter(Channel.status == status)
        sort, column_sorted = self.sortable(q, Channel, field=sort, default='name', direction=direction)
        q = q.order_by(column_sorted)
        if query:
            q = q.filter(db.or_(
                Channel.name.like('%' + query + '%'),
                Channel.url.like('%' + query + '%'),
                Link.alias.like('%' + query + '%'),
                Link.url.like('%' + query + '%'),
                User.name.like('%' + query + '%'),
                User.email.like('%' + query + '%'),
                User.company.like('%' + query + '%'),
                User.contact_name.like('%' + query + '%'),
                User.phone.like('%' + query + '%'),
                User.address.like('%' + query + '%'),
                User.comment.like('%' + query + '%'),
            ))
        return super(ChannelsView, self).get(form=form, default_sort=sort, default_dir=direction, channels=q.all(), **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        try:
            channels = request.form.getlist('channel_ids')
            Link.query.filter(Link.channel_id.in_(channels)).delete(synchronize_session='fetch')
            flash(self._messages['success'], 'success')
            db.session.commit()
            return self.redirect(request.args.get("next", url_for("clients.channels", client_id=extra.get('client_id'), scenario=request.args.get('scenario'))))
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                flash(self._messages['internal_error'], 'error')
            db.session.rollback()
        return super(ChannelsView, self).post(**extra)


class ChannelCreateView(BaseController):
    template = 'clients/channel_create.html'
    # sidebar_path = 'helpers/clients_sidebar.html'
    form = ChannelCreateForm
    filter_form = ChannelFilterForm
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), ('', '', {}), ('', '', {})]
    _messages = {
        'success': _(u'Каналы успешно добавлены'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        scenario_id = int(request.args.get('scenario', None))
        if scenario_id:
            scenario = Scenario.get_or_404(scenario_id)
            self.header += _(u'Добавление каналов для %s' % scenario.name)
            self.header_extend = scenario.client.name
            self.breadcrumbs[1] = (_(u'Сценарии для ') + scenario.client.name, 'clients.scenarios', {'client_id': scenario.client_id})
            self.breadcrumbs[2] = (_(u'Каналы для ') + scenario.name, 'clients.channels', {'client_id': scenario.client_id, 'scenario_id': scenario.get_id()})
            self.breadcrumbs[3] = (_(u'Добавление каналов для ') + scenario.name, '', {})
            return super(ChannelCreateView, self).dispatch_request(client=scenario.client, scenario=scenario, **extra)
        else:
            return self.redirect(url_for("clients.channels.choose", client_id=extra.get('client_id')))

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        filter_form = ChannelCreateFilterForm(request.args, csrf_enabled=False, **extra)
        return super(ChannelCreateView, self).get(form=self.form(request.args, **extra), filter_form=filter_form, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        filter_form = ChannelCreateFilterForm(request.form, csrf_enabled=False, **extra)
        form = self.form(request.form, **extra)
        if form.validate_on_submit():
            scenario = extra.get('scenario')
            try:
                channels = []
                for channel in form.channels.data:
                    if channel.get('checked'):
                        channels.append(Channel.query.filter(db.and_(Channel.id == channel.get('channel_id'))).first())
                for channel in channels:
                    scenario.links.append(Link(channel, scenario))
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("clients.channels", client_id=extra.get('client_id'), scenario_id=extra.get('scenario_id'))))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(ChannelCreateView, self).post(form=form, filter_form=filter_form, **extra)


class ChannelChooseView(BaseController):
    form = ChooseScenarioForm
    header = _(u'Выберите сценарий для добавления каналов клиенту')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), ('', '', {}), ('', '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        client = User.get_or_404(client_id)
        self.header_extend = client.name
        self.breadcrumbs[2] = (_(u'Каналы для ') + client.name, 'clients.channels', {'client_id': client_id})
        self.breadcrumbs[3] = (_(u'Выберите сценарий для добавления каналов клиенту ') + client.name, '', {})
        return super(ChannelChooseView, self).dispatch_request(client=client, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ChannelChooseView, self).get(form=self.form(request.args, **extra), **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        form = self.form(request.form, **extra)
        if form.validate_on_submit():
            return self.redirect(url_for("clients.channels.create", client_id=extra.get('client_id'), scenario=form.scenario.data))
        return super(ChannelChooseView, self).post(form=form, **extra)


class PartnersView(BaseController):
    template = 'clients/partners.html'
    header = _(u'Партнеры')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {})]
    _messages = {
        'success': _(u'Каналы успешно удалены'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        client = User.get_or_404(client_id)
        self.header += _(u' для ') + client.name
        self.header_extend = _(u'для ') + client.name
        self.breadcrumbs[1] = (_(u'Партнеры для ') + client.name, '', '')
        return super(PartnersView, self).dispatch_request(client=client, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = PartnerFilterForm(request.args, csrf_enabled=False, **extra)
        sort = request.args.get('sort', 'name')
        direction = request.args.get('dir', 'desc')
        status = None
        if form.status:
            status = form.status.data
        query = form.query.data
        client_id = extra.get('client_id', None)
        q = User.query.with_entities(
            User,
            db.func.sum(Channel.clicks).label("clicks"),
            db.func.sum(Channel.convs).label("convs"),
            db.func.count(db.func.distinct(Channel.id)).label("channels"),
            db.func.count(db.func.distinct(Scenario.client_id)).label("clients"),
        )\
        .filter(User.role == 'partner')\
        .join(Channel, db.and_(Channel.partner_id == User.id, Channel.status == 'active'))\
        .join(Link, Link.channel_id == Channel.id)\
        .join(Scenario, db.and_(Scenario.id == Link.scenario_id, Scenario.client_id == client_id, Scenario.status == 'active'))\
        .group_by(User.id)
        if status:
            q = q.filter(Channel.status == status)
        sort, column_sorted = self.sortable(q, Channel, field=sort, default='name', direction=direction)
        q = q.order_by(column_sorted)
        if query:
            q = q.filter(db.or_(
                Channel.name.like('%' + query + '%'),
                Channel.url.like('%' + query + '%'),
                Link.alias.like('%' + query + '%'),
                Link.url.like('%' + query + '%'),
                User.name.like('%' + query + '%'),
                User.email.like('%' + query + '%'),
                User.company.like('%' + query + '%'),
                User.contact_name.like('%' + query + '%'),
                User.phone.like('%' + query + '%'),
                User.address.like('%' + query + '%'),
                User.comment.like('%' + query + '%'),
            ))
        users = Pagination(q, extra.get('page', 1), User.per_page)
        return super(PartnersView, self).get(form=form, default_sort=sort, default_dir=direction, users=users, **extra)


class LinkEditView(BaseController):
    header = _(u'Редактирование адреса перехода')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Редактирование адреса перехода'), '', {})]
    _messages = {
        'success': _(u'Сценарий успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        link = Link.query.filter_by(alias=extra.get('alias')).first()
        if not link:
            abort(404)
        scenario = int(request.args.get('scenario', 0))
        if client_id:
            client = User.get_or_404(client_id)
            # self.header += _(u' для ') + client.name
            self.header_extend = _(u'для ') + client.name
            if scenario:
                self.breadcrumbs[1] = (_(u'Каналы для {scenario}'.format(scenario=link.scenario)), 'clients.channels', {'client_id': client_id, 'scenario': scenario})
            else:
                self.breadcrumbs[1] = (_(u'Каналы для {client}'.format(client=client)), 'clients.channels', {'client_id': client_id})
        return super(LinkEditView, self).dispatch_request(scenario=scenario, link=link, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        link = extra.get('link')
        form = LinkEditForm(obj=link)
        return super(LinkEditView, self).get(form=form, header_extend=u"{scenario} {channel}".format(scenario=link.scenario.name, channel=link.channel.name), **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        link = extra.get('link')
        scenario = int(extra.get('scenario'))
        client_id = int(extra.get('client_id'))
        form = LinkEditForm(request.form, obj=scenario)
        if form.validate_on_submit():
            try:
                link.url = form.url.data
                flash(self._messages['success'], 'success')
                db.session.commit()
                return self.redirect(request.args.get("next", url_for("clients.channels", client_id=client_id, scenario=scenario)))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(LinkEditView, self).post(form=form, **extra)


class LinkUrlView(BaseController):
    header = _(u'Получение ссылки перехода')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Получение ссылки перехода'), '', {})]
    _messages = {
        'success': _(u'Сценарий успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        link = Link.query.filter_by(alias=extra.get('alias')).first()
        if not link:
            abort(404)
        scenario = int(request.args.get('scenario', 0))
        if client_id:
            client = User.get_or_404(client_id)
            # self.header += _(u' для ') + client.name
            self.header_extend = _(u'для ') + client.name
            if scenario:
                self.breadcrumbs[1] = (_(u'Каналы для {scenario}'.format(scenario=link.scenario)), 'clients.channels', {'client_id': client_id, 'scenario': scenario})
            else:
                self.breadcrumbs[1] = (_(u'Каналы для {client}'.format(client=client)), 'clients.channels', {'client_id': client_id})
        return super(LinkUrlView, self).dispatch_request(scenario=scenario, link=link, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        link = extra.get('link')
        form = LinkUrlForm(obj=link)
        return super(LinkUrlView, self).get(form=form, header_extend=u"{scenario} {channel}".format(scenario=link.scenario.name, channel=link.channel.name), **extra)


class ClientStatsView(BaseController):

    @roles_accepted('manager', 'admin', 'client')
    def get(self, **extra):
        client_id = extra.get('client_id')
        return self.redirect(url_for('.stats.days', client_id=client_id))


class ClientStatsDaysView(StatsDaysView):
    sidebar_path = "helpers/client_stats_sidebar.html"
    header = _(u'Отчет по дням')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по дням'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        if client_id:
            client = User.get_or_404(client_id)
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Статистика для {client}'.format(client=client)), 'clients.stats', {'client_id': client_id})
        return super(ClientStatsDaysView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ClientStatsDaysFilterForm(request.args, csrf_enabled=False, **extra)
        return super(ClientStatsDaysView, self).get(form=form, **extra)


class ClientStatsScenariosView(StatsScenariosView):
    sidebar_path = "helpers/client_stats_sidebar.html"
    header = _(u'Отчет по сценариям')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по сценариям'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        if client_id:
            client = User.get_or_404(client_id)
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Статистика для {client}'.format(client=client)), 'clients.stats', {'client_id': client_id})
        return super(ClientStatsScenariosView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ClientStatsScenariosFilterForm(request.args, csrf_enabled=False)
        return super(ClientStatsScenariosView, self).get(form=form, **extra)


class ClientStatsPartnersView(StatsPartnersView):
    template = 'stats/partners.html'
    sidebar_path = "helpers/client_stats_sidebar.html"
    header = _(u'Отчет по партнерам')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по партнерам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin', 'client')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        if client_id:
            client = User.get_or_404(client_id)
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Статистика для {client}'.format(client=client)), 'clients.stats', {'client_id': client_id})
        return super(ClientStatsPartnersView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin', 'client')
    def get(self, **extra):
        form = ClientStatsPartnersFilterForm(request.args, csrf_enabled=False, **extra)
        return super(ClientStatsPartnersView, self).get(form=form, **extra)


class ClientStatsChannelsView(StatsChannelsView):
    template = 'stats/channels.html'
    sidebar_path = "helpers/client_stats_sidebar.html"
    header = _(u'Отчет по каналам')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по каналам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        client_id = extra.get('client_id')
        if client_id:
            client = User.get_or_404(client_id)
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Статистика для {client}'.format(client=client)), 'clients.stats', {'client_id': client_id})
        return super(ClientStatsChannelsView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ClientStatsChannelsFilterForm(request.args, csrf_enabled=False)
        return super(ClientStatsChannelsView, self).get(form=form, **extra)


class ScenarioStatsView(BaseController):

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        client_id = extra.get('client_id')
        scenario_id = extra.get('scenario_id')
        return self.redirect(url_for('.stats.days', client_id=client_id, scenario_id=scenario_id))


class ScenarioStatsDaysView(StatsDaysView):
    sidebar_path = "helpers/scenario_stats_sidebar.html"
    header = _(u'Отчет по дням')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по дням'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        scenario_id = extra.get('scenario_id')
        if scenario_id:
            scenario = Scenario.get_or_404(scenario_id)
            client = scenario.client
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Статистика для {scenario}'.format(scenario=scenario)), 'clients.scenario.stats', {'client_id': scenario.client_id, 'scenario_id': scenario.get_id()})
        return super(ScenarioStatsDaysView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ScenarioStatsDaysFilterForm(request.args, csrf_enabled=False)
        return super(ScenarioStatsDaysView, self).get(form=form, **extra)


class ScenarioStatsPartnersView(StatsPartnersView):
    sidebar_path = "helpers/scenario_stats_sidebar.html"
    header = _(u'Отчет по партнерам')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по партнерам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        scenario_id = extra.get('scenario_id')
        if scenario_id:
            scenario = Scenario.get_or_404(scenario_id)
            client = scenario.client
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Статистика для {scenario}'.format(scenario=scenario)), 'clients.scenario.stats', {'client_id': scenario.client_id, 'scenario_id': scenario.get_id()})
        return super(ScenarioStatsPartnersView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ScenarioStatsPartnersFilterForm(request.args, csrf_enabled=False)
        return super(ScenarioStatsPartnersView, self).get(form=form, **extra)


class ScenarioStatsChannelsView(StatsChannelsView):
    sidebar_path = "helpers/scenario_stats_sidebar.html"
    header = _(u'Отчет по каналам')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по каналам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        scenario_id = extra.get('scenario_id')
        if scenario_id:
            scenario = Scenario.get_or_404(scenario_id)
            client = scenario.client
            self.header_extend = _(u'для ') + client.name
            self.breadcrumbs[1] = (_(u'Статистика для {scenario}'.format(scenario=scenario)), 'clients.scenario.stats', {'client_id': scenario.client_id, 'scenario_id': scenario.get_id()})
        return super(ScenarioStatsChannelsView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ScenarioStatsChannelsFilterForm(request.args, csrf_enabled=False)
        return super(ScenarioStatsChannelsView, self).get(form=form, **extra)


clients_view = ClientsView.as_view('index')

clients.add_url_rule('/', defaults={'page': 1}, view_func=clients_view)
clients.add_url_rule('/<int:page>/', view_func=clients_view)
clients.add_url_rule('/create/', view_func=ClientCreateView.as_view('create'))
clients.add_url_rule('/edit/<int:id>/', view_func=ClientEditView.as_view('edit'))
clients.add_url_rule('/delete/<int:id>/', view_func=ClientDeleteView.as_view('delete'))
clients.add_url_rule('/block/<int:id>/', view_func=ClientBlockView.as_view('block'))
clients.add_url_rule('/activate/<int:id>/', view_func=ClientActivateView.as_view('activate'))
clients.add_url_rule('/password/edit/<int:id>/', view_func=ClientPasswordEditView.as_view('password.edit'))
clients.add_url_rule('/code/<int:id>/', view_func=ClientCodeView.as_view('code'))

sections_view = SectionsView.as_view('sections')

clients.add_url_rule('/<int:client_id>/sections/', defaults={'page': 1}, view_func=sections_view)
clients.add_url_rule('/<int:client_id>/sections/<int:page>/', view_func=sections_view)
clients.add_url_rule('/<int:client_id>/sections/create/', view_func=SectionCreateView.as_view('sections.create'))
clients.add_url_rule('/sections/edit/<int:id>/', view_func=SectionEditView.as_view('sections.edit'))
clients.add_url_rule('/sections/delete/<int:id>/', view_func=SectionDeleteView.as_view('sections.delete'))
clients.add_url_rule('/sections/activate/<int:id>/', view_func=SectionActivateView.as_view('sections.activate'))
clients.add_url_rule('/sections/up/<int:id>/', view_func=SectionUpView.as_view('sections.up'))
clients.add_url_rule('/sections/down/<int:id>/', view_func=SectionDownView.as_view('sections.down'))
clients.add_url_rule('/sections/code/<int:id>/', view_func=SectionCodeView.as_view('sections.code'))

scenarios_view = ScenariosView.as_view('scenarios')

clients.add_url_rule('/<int:client_id>/scenarios/', defaults={'page': 1}, view_func=scenarios_view)
clients.add_url_rule('/<int:client_id>/scenarios/<int:page>/', view_func=scenarios_view)
clients.add_url_rule('/<int:client_id>/scenarios/create/', view_func=ScenarioCreateView.as_view('scenarios.create'))
clients.add_url_rule('/scenarios/edit/<int:id>/', view_func=ScenarioEditView.as_view('scenarios.edit'))
clients.add_url_rule('/scenarios/delete/<int:id>/', view_func=ScenarioDeleteView.as_view('scenarios.delete'))
clients.add_url_rule('/scenarios/block/<int:id>/', view_func=ScenarioBlockView.as_view('scenarios.block'))
clients.add_url_rule('/scenarios/activate/<int:id>/', view_func=ScenarioActivateView.as_view('scenarios.activate'))

channels_view = ChannelsView.as_view('channels')

clients.add_url_rule('/<int:client_id>/channels/', defaults={'page': 1}, view_func=channels_view)
clients.add_url_rule('/<int:client_id>/channels/<int:page>/', view_func=channels_view)
clients.add_url_rule('/<int:client_id>/channels/create/', view_func=ChannelCreateView.as_view('channels.create'))
clients.add_url_rule('/<int:client_id>/channels/choose/', view_func=ChannelChooseView.as_view('channels.choose'))


partners_view = PartnersView.as_view('partners')

clients.add_url_rule('/<int:client_id>/partners/', defaults={'page': 1}, view_func=partners_view)
clients.add_url_rule('/<int:client_id>/partners/<int:page>/', view_func=partners_view)

clients.add_url_rule('/<int:client_id>/links/edit/<string:alias>/', view_func=LinkEditView.as_view('links.edit'))
clients.add_url_rule('/<int:client_id>/links/url/<string:alias>/', view_func=LinkUrlView.as_view('links.url'))


clients.add_url_rule('/<int:client_id>/stats/', view_func=ClientStatsView.as_view('stats'))

client_stats_days_view = ClientStatsDaysView.as_view('stats.days')
client_stats_scenarios_view = ClientStatsScenariosView.as_view('stats.scenarios')
client_stats_partners_view = ClientStatsPartnersView.as_view('stats.partners')
client_stats_channels_view = ClientStatsChannelsView.as_view('stats.channels')

clients.add_url_rule('/<int:client_id>/stats/days/', defaults={'page': 1}, view_func=client_stats_days_view)
clients.add_url_rule('/<int:client_id>/stats/days/<int:page>/', view_func=client_stats_days_view)
clients.add_url_rule('/<int:client_id>/stats/scenarios/', defaults={'page': 1}, view_func=client_stats_scenarios_view)
clients.add_url_rule('/<int:client_id>/stats/scenarios/<int:page>/', view_func=client_stats_scenarios_view)
clients.add_url_rule('/<int:client_id>/stats/partners/', defaults={'page': 1}, view_func=client_stats_partners_view)
clients.add_url_rule('/<int:client_id>/stats/partners/<int:page>/', view_func=client_stats_partners_view)
clients.add_url_rule('/<int:client_id>/stats/channels/', defaults={'page': 1}, view_func=client_stats_channels_view)
clients.add_url_rule('/<int:client_id>/stats/channels/<int:page>/', view_func=client_stats_channels_view)


clients.add_url_rule('/<int:client_id>/scenarios/<int:scenario_id>/stats/', view_func=ScenarioStatsView.as_view('scenario.stats'))

scenario_stats_days_view = ScenarioStatsDaysView.as_view('scenario.stats.days')
scenario_stats_partners_view = ScenarioStatsPartnersView.as_view('scenario.stats.partners')
scenario_stats_channels_view = ScenarioStatsChannelsView.as_view('scenario.stats.channels')

clients.add_url_rule('/<int:client_id>/scenarios/<int:scenario_id>/stats/days/', defaults={'page': 1}, view_func=scenario_stats_days_view)
clients.add_url_rule('/<int:client_id>/scenarios/<int:scenario_id>/stats/days/<int:page>/', view_func=scenario_stats_days_view)
clients.add_url_rule('/<int:client_id>/scenarios/<int:scenario_id>/stats/partners/', defaults={'page': 1}, view_func=scenario_stats_partners_view)
clients.add_url_rule('/<int:client_id>/scenarios/<int:scenario_id>/stats/partners/<int:page>/', view_func=scenario_stats_partners_view)
clients.add_url_rule('/<int:client_id>/scenarios/<int:scenario_id>/stats/channels/', defaults={'page': 1}, view_func=scenario_stats_channels_view)
clients.add_url_rule('/<int:client_id>/scenarios/<int:scenario_id>/stats/channels/<int:page>/', view_func=scenario_stats_channels_view)
