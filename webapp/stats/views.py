# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import url_for, request, current_app
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..decorators import roles_accepted
from ..helpers import Pagination
from ..extensions import db
from ..controller import BaseController
from ..models import ReportScenarioChannel, Scenario, Channel, User
from . import stats
from .forms import *


class StatsView(BaseController):

    def get(self, **extra):
        return self.redirect(url_for('.days'))


class StatsDaysView(BaseController):
    template = 'stats/days.html'
    sidebar_path = "helpers/stats_sidebar.html"
    header = _(u'Отчет по дням')
    breadcrumbs = [(_(u'Статистика'), 'stats.index', {}), (_(u'Отчет по дням'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def get(self, **extra):
        direction = request.args.get('dir', 'desc')
        sort = request.args.get('sort', 'day')
        client_id = extra.get('client_id') or int(request.args.get('client', 0))
        scenario_id = extra.get('scenario_id') or int(request.args.get('scenario', 0))
        partner_id = extra.get('partner_id') or int(request.args.get('partner', 0))
        channel_id = extra.get('channel_id') or int(request.args.get('channel', 0))

        if current_user.is_client():
            client_id = current_user.get_id()
        if current_user.is_partner():
            partner_id = current_user.get_id()

        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        if extra.get('form'):
            form = extra.get('form')
            del extra['form']
        else:
            if current_user.is_client():
                form = ClientStatsDaysFilterForm(request.args, csrf_enabled=False)
            elif current_user.is_partner():
                form = PartnerStatsDaysFilterForm(request.args, csrf_enabled=False)
            else:
                form = StatsDaysFilterForm(request.args, csrf_enabled=False)
        date_from = datetime.strptime(form.date_from.data, current_app.config.get('DATE_FORMAT'))
        date_to = datetime.strptime(form.date_to.data, current_app.config.get('DATE_FORMAT'))
        q = ReportScenarioChannel.query.with_entities(
            ReportScenarioChannel.day.label('day'),
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
        )
        total = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
        )
        if date_from and date_to:
            q = q.filter(ReportScenarioChannel.day.between(date_from, date_to))
            total = total.filter(ReportScenarioChannel.day.between(date_from, date_to))
        if client_id:
            q = q.join(Scenario, ReportScenarioChannel.scenario_id == Scenario.id)\
                .filter(Scenario.client_id == client_id)
            total = total.join(Scenario, ReportScenarioChannel.scenario_id == Scenario.id)\
                .filter(Scenario.client_id == client_id)
        if scenario_id:
            q = q.filter(ReportScenarioChannel.scenario_id == scenario_id)
            total = total.filter(ReportScenarioChannel.scenario_id == scenario_id)
        if partner_id:
            q = q.join(Channel, db.and_(ReportScenarioChannel.channel_id == Channel.id, Channel.partner_id == partner_id))
            total = total.join(Channel, db.and_(ReportScenarioChannel.channel_id == Channel.id, Channel.partner_id == partner_id))
        if channel_id:
            q = q.filter(ReportScenarioChannel.channel_id == channel_id)
            total = total.filter(ReportScenarioChannel.channel_id == channel_id)
        q = q.group_by(ReportScenarioChannel.day)
        sort, column_sorted = self.sortable(q, ReportScenarioChannel, field=sort, default='day', direction=direction)
        q = q.order_by(column_sorted)
        stats = Pagination(q, extra.get('page', 1), ReportScenarioChannel.per_page)
        return super(StatsDaysView, self).get(form=form, default_sort=sort, default_dir=direction, stats=stats, total=total.first(), **extra)


class StatsPartnersView(BaseController):
    template = 'stats/partners.html'
    sidebar_path = "helpers/stats_sidebar.html"
    header = _(u'Отчет по партнерам')
    breadcrumbs = [(_(u'Статистика'), 'stats.index', {}), (_(u'Отчет по партнерам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin', 'client')
    def get(self, **extra):
        direction = request.args.get('dir', 'asc')
        sort = request.args.get('sort', 'name')
        client_id = extra.get('client_id') or int(request.args.get('client', 0))
        scenario_id = extra.get('scenario_id') or int(request.args.get('scenario', 0))

        if current_user.is_client():
            client_id = current_user.get_id()

        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        if extra.get('form'):
            form = extra.get('form')
            del extra['form']
        else:
            if current_user.is_client():
                form = ClientStatsPartnersFilterForm(request.args, csrf_enabled=False)
            elif current_user.is_partner():
                form = PartnerStatsPartnersFilterForm(request.args, csrf_enabled=False)
            else:
                form = StatsPartnersFilterForm(request.args, csrf_enabled=False)
        date_from = datetime.strptime(form.date_from.data, current_app.config.get('DATE_FORMAT'))
        date_to = datetime.strptime(form.date_to.data, current_app.config.get('DATE_FORMAT'))
        q = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
            User.name.label("name"),
            User.email.label("email"),
        )\
        .join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id))\
        .join(User, db.and_(Channel.partner_id == User.id, User.role == 'partner'))
        total = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
        )\
        .join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id))\
        .join(User, db.and_(Channel.partner_id == User.id, User.role == 'partner'))
        if date_from and date_to:
            q = q.filter(ReportScenarioChannel.day.between(date_from, date_to))
            total = total.filter(ReportScenarioChannel.day.between(date_from, date_to))
        if client_id:
            q = q.join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id, Scenario.client_id == client_id))
            total = total.join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id, Scenario.client_id == client_id))
        if scenario_id:
            q = q.filter(ReportScenarioChannel.scenario_id == scenario_id)
            total = q.filter(ReportScenarioChannel.scenario_id == scenario_id)
        q = q.group_by(Channel.partner_id)
        sort, column_sorted = self.sortable(q, User, field=sort, default='name', direction=direction)
        q = q.order_by(column_sorted)
        stats = Pagination(q, extra.get('page', 1), ReportScenarioChannel.per_page)
        return super(StatsPartnersView, self).get(form=form, default_sort=sort, default_dir=direction, stats=stats, total=total.first(), **extra)


class StatsChannelsView(BaseController):
    template = 'stats/channels.html'
    sidebar_path = "helpers/stats_sidebar.html"
    header = _(u'Отчет по каналам')
    breadcrumbs = [(_(u'Статистика'), 'stats.index', {}), (_(u'Отчет по каналам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin', 'client', 'partner')
    def get(self, **extra):
        direction = request.args.get('dir', 'asc')
        sort = request.args.get('sort', 'name')
        client_id = extra.get('client_id') or int(request.args.get('client', 0))
        scenario_id = extra.get('scenario_id') or int(request.args.get('scenario', 0))
        partner_id = extra.get('partner_id') or int(request.args.get('partner', 0))

        if current_user.is_client():
            client_id = current_user.get_id()
        if current_user.is_partner():
            partner_id = current_user.get_id()

        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        if extra.get('form'):
            form = extra.get('form')
            del extra['form']
        else:
            if current_user.is_client():
                form = ClientStatsChannelsFilterForm(request.args, csrf_enabled=False)
            elif current_user.is_partner():
                form = PartnerStatsChannelsFilterForm(request.args, csrf_enabled=False)
            else:
                form = StatsChannelsFilterForm(request.args, csrf_enabled=False)
        date_from = datetime.strptime(form.date_from.data, current_app.config.get('DATE_FORMAT'))
        date_to = datetime.strptime(form.date_to.data, current_app.config.get('DATE_FORMAT'))
        q = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
            db.func.concat(User.name, ' : ', Channel.name).label("name"),
            User.email.label("email"),
        )\
        .join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id))\
        .join(User, db.and_(Channel.partner_id == User.id, User.role == 'partner'))
        total = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
        )\
        .join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id))\
        .join(User, db.and_(Channel.partner_id == User.id, User.role == 'partner'))
        if date_from and date_to:
            q = q.filter(ReportScenarioChannel.day.between(date_from, date_to))
            total = total.filter(ReportScenarioChannel.day.between(date_from, date_to))
        if client_id:
            q = q.join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id, Scenario.client_id == client_id))
            total = total.join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id, Scenario.client_id == client_id))
        if scenario_id:
            q = q.filter(ReportScenarioChannel.scenario_id == scenario_id)
            total = total.filter(ReportScenarioChannel.scenario_id == scenario_id)
        if partner_id:
            q = q.join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id, Channel.partner_id == partner_id))
            total = total.join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id, Channel.partner_id == partner_id))
        q = q.group_by(Channel.id)
        sort, column_sorted = self.sortable(q, User, field=sort, default='name', direction=direction)
        q = q.order_by(column_sorted)
        stats = Pagination(q, extra.get('page', 1), ReportScenarioChannel.per_page)
        return super(StatsChannelsView, self).get(form=form, default_sort=sort, default_dir=direction, stats=stats, total=total.first(), **extra)


class StatsClientsView(BaseController):
    template = 'stats/clients.html'
    sidebar_path = "helpers/stats_sidebar.html"
    header = _(u'Отчет по клиентам')
    breadcrumbs = [(_(u'Статистика'), 'stats.index', {}), (_(u'Отчет по клиентам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin', 'partner')
    def get(self, **extra):
        direction = request.args.get('dir', 'desc')
        sort = request.args.get('sort', 'name')
        partner_id = extra.get('partner_id') or int(request.args.get('partner', 0))
        channel_id = extra.get('channel_id') or int(request.args.get('channel', 0))

        if current_user.is_partner():
            partner_id = current_user.get_id()

        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        if extra.get('form'):
            form = extra.get('form')
            del extra['form']
        else:
            if current_user.is_client():
                form = ClientStatsClientsFilterForm(request.args, csrf_enabled=False)
            elif current_user.is_partner():
                form = PartnerStatsClientsFilterForm(request.args, csrf_enabled=False)
            else:
                form = StatsClientsFilterForm(request.args, csrf_enabled=False)
        date_from = datetime.strptime(form.date_from.data, current_app.config.get('DATE_FORMAT'))
        date_to = datetime.strptime(form.date_to.data, current_app.config.get('DATE_FORMAT'))
        q = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
            User.name.label('name'),
        )\
        .join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id))\
        .join(User, db.and_(Scenario.client_id == User.id, User.role == 'client'))
        total = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
        )\
        .join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id))\
        .join(User, db.and_(Scenario.client_id == User.id, User.role == 'client'))
        if date_from and date_to:
            q = q.filter(ReportScenarioChannel.day.between(date_from, date_to))
            total = total.filter(ReportScenarioChannel.day.between(date_from, date_to))
        if partner_id:
            q = q.join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id, Channel.partner_id == partner_id))
            total = total.join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id, Channel.partner_id == partner_id))
        if channel_id:
            q = q.filter(ReportScenarioChannel.channel_id == channel_id)
            total = total.filter(ReportScenarioChannel.channel_id == channel_id)
        q = q.group_by(User.id)
        sort, column_sorted = self.sortable(q, User, field=sort, default='name', direction=direction)
        q = q.order_by(column_sorted)
        stats = Pagination(q, extra.get('page', 1), ReportScenarioChannel.per_page)
        return super(StatsClientsView, self).get(form=form, default_sort=sort, default_dir=direction, stats=stats, total=total.first(), **extra)


class StatsScenariosView(BaseController):
    template = 'stats/scenarios.html'
    sidebar_path = "helpers/stats_sidebar.html"
    header = _(u'Отчет по сценариям')
    breadcrumbs = [(_(u'Статистика'), 'stats.index', {}), (_(u'Отчет по сценариям'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def get(self, **extra):
        direction = request.args.get('dir', 'desc')
        sort = request.args.get('sort', 'name')
        client_id = extra.get('client_id') or int(request.args.get('client', 0))
        partner_id = extra.get('partner_id') or int(request.args.get('partner', 0))
        channel_id = extra.get('channel_id') or int(request.args.get('channel', 0))

        if current_user.is_client():
            client_id = current_user.get_id()
        if current_user.is_partner():
            partner_id = current_user.get_id()

        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        if extra.get('form'):
            form = extra.get('form')
            del extra['form']
        else:
            if current_user.is_client():
                form = ClientStatsScenariosFilterForm(request.args, csrf_enabled=False)
            elif current_user.is_partner():
                form = PartnerStatsScenariosFilterForm(request.args, csrf_enabled=False)
            else:
                form = StatsScenariosFilterForm(request.args, csrf_enabled=False)
        date_from = datetime.strptime(form.date_from.data, current_app.config.get('DATE_FORMAT'))
        date_to = datetime.strptime(form.date_to.data, current_app.config.get('DATE_FORMAT'))
        q = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
            db.func.concat(User.name, ' : ', Scenario.name).label("name"),
            User.email.label("email"),
        )\
        .join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id))\
        .join(User, db.and_(Scenario.client_id == User.id, User.role == 'client'))
        total = ReportScenarioChannel.query.with_entities(
            db.func.sum(ReportScenarioChannel.clicks).label("clicks"),
            db.func.sum(ReportScenarioChannel.convs).label("convs"),
            db.func.sum(ReportScenarioChannel.cost).label("cost"),
            db.func.sum(ReportScenarioChannel.payout).label("payout"),
            db.func.sum(ReportScenarioChannel.cost - ReportScenarioChannel.payout).label("income"),
        )\
        .join(Scenario, db.and_(Scenario.id == ReportScenarioChannel.scenario_id))\
        .join(User, db.and_(Scenario.client_id == User.id, User.role == 'client'))
        if date_from and date_to:
            q = q.filter(ReportScenarioChannel.day.between(date_from, date_to))
            total = total.filter(ReportScenarioChannel.day.between(date_from, date_to))
        if client_id:
            q = q.filter(User.id == client_id)
            total = total.filter(User.id == client_id)
        if partner_id:
            q = q.join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id, Channel.partner_id == partner_id))
            total = total.join(Channel, db.and_(Channel.id == ReportScenarioChannel.channel_id, Channel.partner_id == partner_id))
        if channel_id:
            q = q.filter(ReportScenarioChannel.channel_id == channel_id)
            total = total.filter(ReportScenarioChannel.channel_id == channel_id)
        q = q.group_by(Scenario.id)
        sort, column_sorted = self.sortable(q, User, field=sort, default='name', direction=direction)
        if sort == 'name':
            q = q.order_by(User.name, column_sorted)
        else:
            q = q.order_by(column_sorted)
        stats = Pagination(q, extra.get('page', 1), ReportScenarioChannel.per_page)
        return super(StatsScenariosView, self).get(form=form, default_sort=sort, default_dir=direction, stats=stats, total=total.first(), **extra)

stats.add_url_rule('/', view_func=StatsView.as_view('index'))

days_view = StatsDaysView.as_view('days')
partners_view = StatsPartnersView.as_view('partners')
channels_view = StatsChannelsView.as_view('channels')
clients_view = StatsClientsView.as_view('clients')
scenarios_view = StatsScenariosView.as_view('scenarios')

stats.add_url_rule('/days/', defaults={'page': 1}, view_func=days_view)
stats.add_url_rule('/days/<int:page>/', view_func=days_view)

stats.add_url_rule('/partners/', defaults={'page': 1}, view_func=partners_view)
stats.add_url_rule('/partners/<int:page>/', view_func=partners_view)

stats.add_url_rule('/channels/', defaults={'page': 1}, view_func=channels_view)
stats.add_url_rule('/channels/<int:page>/', view_func=channels_view)

stats.add_url_rule('/clients/', defaults={'page': 1}, view_func=clients_view)
stats.add_url_rule('/clients/<int:page>/', view_func=clients_view)

stats.add_url_rule('/scenarios/', defaults={'page': 1}, view_func=scenarios_view)
stats.add_url_rule('/scenarios/<int:page>/', view_func=scenarios_view)
