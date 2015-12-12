# -*- coding: utf-8 -*-
from flask import url_for, request, flash, current_app, jsonify
from flask.ext.babel import gettext as _
from ..controller import BaseController
from ..extensions import db
from ..decorators import roles_accepted
from ..helpers import Pagination
from .forms import *
from ..models import User, Scenario, Channel, Link
from ..users.views import UsersView, UserCreateView, UserEditView, UserPasswordEditView, UserDeleteView, UserBlockView, UserActivateView
from ..stats.views import StatsDaysView, StatsClientsView, StatsChannelsView, StatsScenariosView
from ..dictionary import *
from . import partners

STATUSES_BLOCKED = [k[0] for k in STATUSES_BLOCKED]


class PartnersView(UsersView):
    role = 'partner'
    template = 'partners.html'
    header = _(u'Партнеры')
    breadcrumbs = [(_(u'Партнеры'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(PartnersView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        return super(PartnersView, self).post(**extra)


class PartnerCreateView(UserCreateView):
    role = 'partner'
    header = _(u'Добавление партнера')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), (_(u'Добавление партнера'), '', {})]
    _messages = {
        'success': _(u'Партнер успешно добавлен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin', 'manager')
    def get(self, **extra):
        return super(PartnerCreateView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        self.redirect_url = url_for('partners.index')
        return super(PartnerCreateView, self).post(**extra)


class PartnerEditView(UserEditView):
    role = 'partner'
    header = _(u'Редактирование партнера')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), (_(u'Редактирование партнера'), '', {})]
    _messages = {
        'success': _(u'Партнер успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(PartnerEditView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        self.redirect_url = url_for('partners.index')
        return super(PartnerEditView, self).post(**extra)


class PartnerPasswordEditView(UserPasswordEditView):
    role = 'partner'
    header = _(u'Смена пароля у партнера')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), (_(u'Смена пароля'), '', {})]
    _messages = {
        'success': _(u'Пароль успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(PartnerPasswordEditView, self).get(**extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        self.redirect_url = url_for('partners.index')
        return super(PartnerPasswordEditView, self).post(**extra)


class PartnerDeleteView(UserDeleteView):
    _messages = {
        'success': _(u'Партнер успешно удален'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for('partners.index')
        return super(PartnerDeleteView, self).get(**extra)


class PartnerBlockView(UserBlockView):
    _messages = {
        'success': _(u'Партнер успешно заблокирован'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for('partners.index')
        return super(PartnerBlockView, self).get(**extra)


class PartnerActivateView(UserActivateView):
    _messages = {
        'success': _(u'Партнер успешно активирован'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('admin')
    def get(self, **extra):
        self.redirect_url = url_for('partners.index')
        return super(PartnerActivateView, self).get(**extra)


class ChannelsView(BaseController):
    template = 'partners/channels.html'
    header = _(u'Каналы')
    breadcrumbs = [(_(u'Партеры'), 'partners.index', {}), (_(u'Каналы'), '', {})]

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id')
        partner = User.get_or_404(partner_id)
        self.header += _(u' для ') + partner.name
        self.header_extend = _(u'для ') + partner.name
        self.breadcrumbs[1] = (_(u'Каналы для ') + partner.name, '', '')
        return super(ChannelsView, self).dispatch_request(partner=partner, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ChannelFilterForm(request.args, csrf_enabled=False, **extra)
        sort = request.args.get('sort', 'name')
        direction = request.args.get('dir', 'asc')
        status = None
        if form.status:
            status = form.status.data
        query = form.query.data
        partner_id = extra.get('partner_id', None)
        client_id = int(request.args.get('client', 0))
        no_client_id = int(request.args.get('no_client', 0))
        q = Channel.query
        if client_id:
            q = q.join(Link, Link.channel_id == Channel.id)\
                .join(Scenario, db.and_(Link.scenario_id == Scenario.id, Scenario.client_id == client_id, Scenario.status == 'active'))\
                .group_by(Channel.id)
        if no_client_id:
            q = q.join(Link, Link.channel_id == Channel.id)\
                .join(Scenario, db.and_(Link.scenario_id == Scenario.id, Scenario.client_id != no_client_id, Scenario.status == 'active'))\
                .group_by(Channel.id)
        if status:
            q = q.filter(Channel.status == status)
        if partner_id:
            q = q.filter(Channel.partner_id == partner_id)

        sort, column_sorted = self.sortable(q, Channel, field=sort, default='id', direction=direction)
        q = q.order_by(column_sorted)
        if query:
            q = q.filter(db.or_(
                Channel.name.like('%' + query + '%'),
                Channel.channel_type.like('%' + query + '%'),
                Channel.url.like('%' + query + '%'),
            ))
        channels = q.paginate(extra.get('page', 1), Channel.per_page, False)
        return super(ChannelsView, self).get(form=form, default_sort=sort, default_dir=direction, channels=channels, **extra)


class ChannelCreateView(BaseController):
    form = ChannelCreateForm
    header = _(u'Добавление канала')
    header_extend = ''
    breadcrumbs = [(_(u'Партеры'), 'partners.index', {}), (_(u'Каналы'), 'partners.channels', {}), (_(u'Добавление канала'), '', {})]
    _messages = {
        'success': _(u'Канал успешно добавлен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id', None)
        if partner_id:
            partner = User.get_or_404(partner_id)
            self.header_extend = _(u'для ') + partner.name
            self.breadcrumbs[1] = (_(u'Каналы для ') + partner.name, 'partners.channels', {'partner_id': partner_id})
        return super(ChannelCreateView, self).dispatch_request(partner=partner, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        return super(ChannelCreateView, self).get(form=self.form(request.args, **extra), header_extend=self.header_extend, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        partner_id = extra.get('partner_id')
        form = self.form(request.form, **extra)
        if form.validate_on_submit():
            try:
                channel = Channel(
                    partner_id=partner_id,
                    name=form.name.data,
                    channel_type=form.channel_type.data,
                    url=form.url.data,
                    price=form.price.data * 100,
                )
                db.session.add(channel)
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("partners.channels", partner_id=partner_id)))
            except Exception, e:
                flash(self._messages['success'], 'success')
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(ChannelCreateView, self).post(form=form, **extra)


class ChannelEditView(BaseController):
    header = _(u'Редактирование канала')
    header_extend = ''
    breadcrumbs = [(_(u'Партеры'), 'partners.index', {}), (_(u'Каналы'), 'partners.channels', {}), (_(u'Редактирование канала'), '', {})]
    _messages = {
        'success': _(u'Канал успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        channel = Channel.get_or_404(extra.get('id'))
        channel.price = float(channel.get_price())
        partner = channel.partner
        self.header_extend = _(u'для ') + partner.name
        self.breadcrumbs[1] = (_(u'Каналы для ') + partner.name, 'partners.channels', {'partner_id': channel.partner_id})
        return super(ChannelEditView, self).dispatch_request(partner_id=channel.partner_id, channel=channel, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        channel = extra.get('channel')
        form = ChannelEditForm(obj=channel)
        form.populate_obj(channel)
        return super(ChannelEditView, self).get(form=form, header_extend=self.header_extend, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        channel = extra.get('channel')
        form = ChannelEditForm(request.form, obj=channel)
        if form.validate_on_submit():
            form.populate_obj(channel)
            try:
                result = channel.update(
                    name=form.name.data,
                    channel_type=form.channel_type.data,
                    url=form.url.data,
                    price=form.price.data * 100,
                )
                if not result:
                    raise Exception('not save')
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next", url_for("partners.channels", partner_id=channel.partner_id)))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(ChannelEditView, self).post(form=form, header_extend=self.header_extend, **extra)


class ChannelActivateView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            channel = Channel.query.get_or_404(extra.get('id'))
            channel.activate()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ChannelBlockView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            channel = Channel.query.get_or_404(extra.get('id'))
            channel.block()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ChannelDeleteView(BaseController):

    @roles_accepted('admin')
    def post(self, **extra):
        try:
            channel = Channel.query.get_or_404(extra.get('id'))
            channel.delete()
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ClientsView(BaseController):
    template = 'partners/clients.html'
    header = _(u'Клиенты')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {})]
    _messages = {
        'success': _(u'Каналы успешно удалены'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id')
        partner = User.get_or_404(partner_id)
        self.header += _(u' для ') + partner.name
        self.header_extend = _(u'для ') + partner.name
        self.breadcrumbs[1] = (_(u'Клиенты для ') + partner.name, '', '')
        return super(ClientsView, self).dispatch_request(partner=partner, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ClientFilterForm(request.args, csrf_enabled=False, **extra)
        sort = request.args.get('sort', 'name')
        direction = request.args.get('dir', 'asc')
        status = None
        if form.status:
            status = form.status.data
        query = form.query.data
        partner_id = extra.get('partner_id', None)
        q = User.query.with_entities(
            User,
            db.func.sum(Scenario.clicks).label("clicks"),
            db.func.sum(Scenario.convs).label("convs"),
            db.func.count(db.func.distinct(Link.channel_id)).label("channels"),
            db.func.count(db.func.distinct(Channel.partner_id)).label("partners"),
        )\
        .filter(User.role == 'client')\
        .join(Scenario, db.and_(Scenario.client_id == User.id))\
        .join(Link, Link.scenario_id == Scenario.id)\
        .join(Channel, db.and_(Channel.id == Link.channel_id, Channel.partner_id == partner_id))\
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
        return super(ClientsView, self).get(form=form, default_sort=sort, default_dir=direction, users=users, **extra)


class ScenariosView(BaseController):
    template = 'partners/scenarios.html'
    header = _(u'Сценарии')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {}), ('', '', {})]
    _messages = {
        'success': _(u'Каналы успешно удалены'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id')
        channel = int(request.args.get('channel', 0))
        partner = User.get_or_404(partner_id)
        self.header += _(u' для ') + partner.name
        self.header_extend = _(u'для ') + partner.name
        if channel:
            self.breadcrumbs[1] = (_(u'Каналы для ') + partner.name, 'partners.channels', {'partner_id': partner_id})
            self.breadcrumbs[2] = (_(u'Сценарии для ') + partner.name, '', '')
        else:
            self.breadcrumbs[1] = (_(u'Сценарии для ') + partner.name, '', '')
            self.breadcrumbs[2] = ('', '', '')
        return super(ScenariosView, self).dispatch_request(channel=channel, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ScenarioFilterForm(request.args, csrf_enabled=False, **extra)
        sort = request.args.get('sort', 'name')
        direction = request.args.get('dir', 'asc')
        status = None
        if form.status:
            status = form.status.data
        query = form.query.data
        partner_id = extra.get('partner_id', None)
        if form.channel:
            channel_id = form.channel.data
        if channel_id:
            q = Scenario.query.with_entities(Scenario, Link)\
                .join(Link, db.and_(Link.scenario_id == Scenario.id, Link.channel_id == channel_id, Link.url != ''))\
                .join(Channel, db.and_(Channel.id == Link.channel_id, Channel.partner_id == partner_id))\
                .join(User, User.id == Channel.partner_id)\
                .group_by(Scenario.id)
        else:
            q = Scenario.query.with_entities(Scenario, Link)\
                .join(Link, db.and_(Link.scenario_id == Scenario.id, Link.url != ''))\
                .join(Channel, db.and_(Channel.id == Link.channel_id, Channel.partner_id == partner_id))\
                .join(User, User.id == Channel.partner_id)\
                .group_by(Scenario.id)
        if status:
            q = q.filter(Scenario.status == status)
        sort, column_sorted = self.sortable(q, Channel, field=sort, default='name', direction=direction)
        q = q.order_by(column_sorted)
        if query:
            q = q.filter(db.or_(
                Scenario.name.like('%' + query + '%'),
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
        return super(ScenariosView, self).get(form=form, default_sort=sort, default_dir=direction, scenarios=q.all(), **extra)


class LinkUrlView(BaseController):
    header = _(u'Получение ссылки перехода')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {}), (_(u'Получение ссылки перехода'), '', {})]
    _messages = {
        'success': _(u'Сценарий успешно сохранен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id')
        link = Link.query.filter_by(alias=extra.get('alias')).first()
        if not link:
            abort(404)
        channel = int(request.args.get('channel', 0))
        if partner_id:
            partner = User.get_or_404(partner_id)
            # self.header += _(u' для ') + client.name
            self.header_extend = _(u'для ') + partner.name
            if channel:
                self.breadcrumbs[1] = (_(u'Сценарии для {channel}'.format(channel=link.channel)), 'partners.scenarios', {'partner_id': partner_id, 'channel': channel})
            else:
                self.breadcrumbs[1] = (_(u'Каналы для {partner}'.format(partner=partner)), 'partners.channels', {'partner_id': partner_id})
        return super(LinkUrlView, self).dispatch_request(channel=channel, link=link, **extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        link = extra.get('link')
        form = LinkUrlForm(obj=link)
        return super(LinkUrlView, self).get(form=form, header_extend=u"{scenario} {channel}".format(scenario=link.scenario.name, channel=link.channel.name), **extra)


class PartnerStatsView(BaseController):

    @roles_accepted('manager', 'admin', 'partner')
    def get(self, **extra):
        partner_id = extra.get('partner_id')
        return self.redirect(url_for('.stats.days', partner_id=partner_id))


class PartnerStatsDaysView(StatsDaysView):
    sidebar_path = "helpers/partner_stats_sidebar.html"
    header = _(u'Отчет по дням')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {}), (_(u'Отчет по дням'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id')
        if partner_id:
            partner = User.get_or_404(partner_id)
            self.header_extend = _(u'для ') + partner.name
            self.breadcrumbs[1] = (_(u'Статистика для {partner}'.format(partner=partner)), 'partners.stats', {'partner_id': partner_id})
        return super(PartnerStatsDaysView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = PartnerStatsDaysFilterForm(request.args, csrf_enabled=False, **extra)
        return super(PartnerStatsDaysView, self).get(form=form, **extra)


class PartnerStatsClientsView(StatsClientsView):
    template = 'stats/clients.html'
    sidebar_path = "helpers/partner_stats_sidebar.html"
    header = _(u'Отчет по клиентам')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {}), (_(u'Отчет по клиентам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id')
        if partner_id:
            partner = User.get_or_404(partner_id)
            self.header_extend = _(u'для ') + partner.name
            self.breadcrumbs[1] = (_(u'Статистика для {partner}'.format(partner=partner)), 'partners.stats', {'partner_id': partner_id})
        return super(PartnerStatsClientsView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = PartnerStatsClientsFilterForm(request.args, csrf_enabled=False, **extra)
        return super(PartnerStatsClientsView, self).get(form=form, **extra)


class PartnerStatsChannelsView(StatsChannelsView):
    template = 'stats/channels.html'
    sidebar_path = "helpers/partner_stats_sidebar.html"
    header = _(u'Отчет по каналам')
    breadcrumbs = [(_(u'Клиенты'), 'clients.index', {}), ('', '', {}), (_(u'Отчет по каналам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        partner_id = extra.get('partner_id')
        if partner_id:
            partner = User.get_or_404(partner_id)
            self.header_extend = _(u'для ') + partner.name
            self.breadcrumbs[1] = (_(u'Статистика для {partner}'.format(partner=partner)), 'partners.stats', {'partner_id': partner_id})
        return super(PartnerStatsChannelsView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = PartnerStatsChannelsFilterForm(request.args, csrf_enabled=False)
        return super(PartnerStatsChannelsView, self).get(form=form, **extra)


class ChannelStatsView(BaseController):

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        partner_id = extra.get('partner_id')
        channel_id = extra.get('channel_id')
        return self.redirect(url_for('.stats.days', partner_id=partner_id, channel_id=channel_id))


class ChannelStatsDaysView(StatsDaysView):
    sidebar_path = "helpers/channel_stats_sidebar.html"
    header = _(u'Отчет по дням')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {}), (_(u'Отчет по дням'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        channel_id = extra.get('channel_id')
        if channel_id:
            channel = Channel.get_or_404(channel_id)
            partner = channel.partner
            self.header_extend = _(u'для ') + partner.name
            self.breadcrumbs[1] = (_(u'Статистика для {channel}'.format(channel=channel)), 'partners.channel.stats', {'partner_id': channel.partner_id, 'channel_id': channel.get_id()})
        return super(ChannelStatsDaysView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ChannelStatsDaysFilterForm(request.args, csrf_enabled=False)
        return super(ChannelStatsDaysView, self).get(form=form, **extra)


class ChannelStatsClientsView(StatsClientsView):
    sidebar_path = "helpers/channel_stats_sidebar.html"
    header = _(u'Отчет по клиентам')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {}), (_(u'Отчет по клиентам'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        channel_id = extra.get('channel_id')
        if channel_id:
            channel = Channel.get_or_404(channel_id)
            partner = channel.partner
            self.header_extend = _(u'для ') + partner.name
            self.breadcrumbs[1] = (_(u'Статистика для {channel}'.format(channel=channel)), 'partners.channel.stats', {'partner_id': channel.partner_id, 'channel_id': channel.get_id()})
        return super(ChannelStatsClientsView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ChannelStatsClientsFilterForm(request.args, csrf_enabled=False)
        return super(ChannelStatsClientsView, self).get(form=form, **extra)


class ChannelStatsScenariosView(StatsScenariosView):
    sidebar_path = "helpers/channel_stats_sidebar.html"
    header = _(u'Отчет по сценариям')
    breadcrumbs = [(_(u'Партнеры'), 'partners.index', {}), ('', '', {}), (_(u'Отчет по сценариям'), '', {})]
    _messages = {
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def dispatch_request(self, **extra):
        channel_id = extra.get('channel_id')
        if channel_id:
            channel = Channel.get_or_404(channel_id)
            partner = channel.partner
            self.header_extend = _(u'для ') + partner.name
            self.breadcrumbs[1] = (_(u'Статистика для {channel}'.format(channel=channel)), 'partners.channel.stats', {'partner_id': channel.partner_id, 'channel_id': channel.get_id()})
        return super(ChannelStatsScenariosView, self).dispatch_request(**extra)

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        form = ChannelStatsScenariosFilterForm(request.args, csrf_enabled=False)
        return super(ChannelStatsScenariosView, self).get(form=form, **extra)


partners_view = PartnersView.as_view('index')

partners.add_url_rule('/', defaults={'page': 1}, view_func=partners_view)
partners.add_url_rule('/<int:page>/', view_func=partners_view)
partners.add_url_rule('/create/', view_func=PartnerCreateView.as_view('create'))
partners.add_url_rule('/edit/<int:id>/', view_func=PartnerEditView.as_view('edit'))
partners.add_url_rule('/delete/<int:id>/', view_func=PartnerDeleteView.as_view('delete'))
partners.add_url_rule('/block/<int:id>/', view_func=PartnerBlockView.as_view('block'))
partners.add_url_rule('/activate/<int:id>/', view_func=PartnerActivateView.as_view('activate'))
partners.add_url_rule('/password/edit/<int:id>/', view_func=PartnerPasswordEditView.as_view('password.edit'))


channels_view = ChannelsView.as_view('channels')
channels_create_view = ChannelCreateView.as_view('channels.create')

partners.add_url_rule('/<int:partner_id>/channels/', defaults={'page': 1}, view_func=channels_view)
partners.add_url_rule('/<int:partner_id>/channels/<int:page>/', view_func=channels_view)
partners.add_url_rule('/<int:partner_id>/channels/create/', view_func=channels_create_view)
partners.add_url_rule('/channels/edit/<int:id>/', view_func=ChannelEditView.as_view('channels.edit'))
partners.add_url_rule('/channels/delete/<int:id>/', view_func=ChannelDeleteView.as_view('channels.delete'))
partners.add_url_rule('/channels/block/<int:id>/', view_func=ChannelBlockView.as_view('channels.block'))
partners.add_url_rule('/channels/activate/<int:id>/', view_func=ChannelActivateView.as_view('channels.activate'))

clients_view = ClientsView.as_view('clients')

partners.add_url_rule('/<int:partner_id>/clients/', defaults={'page': 1}, view_func=clients_view)
partners.add_url_rule('/<int:partner_id>/clients/<int:page>/', view_func=clients_view)

scenarios_view = ScenariosView.as_view('scenarios')

partners.add_url_rule('/<int:partner_id>/scenarios/', defaults={'page': 1}, view_func=scenarios_view)
partners.add_url_rule('/<int:partner_id>/scenarios/<int:page>/', view_func=scenarios_view)

partners.add_url_rule('/<int:partner_id>/links/url/<string:alias>/', view_func=LinkUrlView.as_view('links.url'))

partners.add_url_rule('/<int:partner_id>/stats/', view_func=PartnerStatsView.as_view('stats'))

partner_stats_days_view = PartnerStatsDaysView.as_view('stats.days')
partner_stats_clients_view = PartnerStatsClientsView.as_view('stats.clients')
partner_stats_channels_view = PartnerStatsChannelsView.as_view('stats.channels')

partners.add_url_rule('/<int:partner_id>/stats/days/', defaults={'page': 1}, view_func=partner_stats_days_view)
partners.add_url_rule('/<int:partner_id>/stats/days/<int:page>/', view_func=partner_stats_days_view)
partners.add_url_rule('/<int:partner_id>/stats/clients/', defaults={'page': 1}, view_func=partner_stats_clients_view)
partners.add_url_rule('/<int:partner_id>/stats/clients/<int:page>/', view_func=partner_stats_clients_view)
partners.add_url_rule('/<int:partner_id>/stats/channels/', defaults={'page': 1}, view_func=partner_stats_channels_view)
partners.add_url_rule('/<int:partner_id>/stats/channels/<int:page>/', view_func=partner_stats_channels_view)

partners.add_url_rule('/<int:partner_id>/channels/<int:channel_id>/stats/', view_func=ChannelStatsView.as_view('channel.stats'))

channel_stats_days_view = ChannelStatsDaysView.as_view('channel.stats.days')
channel_stats_clients_view = ChannelStatsClientsView.as_view('channel.stats.clients')
channel_stats_scenarios_view = ChannelStatsScenariosView.as_view('channel.stats.scenarios')

partners.add_url_rule('/<int:partner_id>/channels/<int:channel_id>/stats/days/', defaults={'page': 1}, view_func=channel_stats_days_view)
partners.add_url_rule('/<int:partner_id>/channels/<int:channel_id>/stats/days/<int:page>/', view_func=channel_stats_days_view)
partners.add_url_rule('/<int:partner_id>/channels/<int:channel_id>/stats/clients/', defaults={'page': 1}, view_func=channel_stats_clients_view)
partners.add_url_rule('/<int:partner_id>/channels/<int:channel_id>/stats/clients/<int:page>/', view_func=channel_stats_clients_view)
partners.add_url_rule('/<int:partner_id>/channels/<int:channel_id>/stats/scenarios/', defaults={'page': 1}, view_func=channel_stats_scenarios_view)
partners.add_url_rule('/<int:partner_id>/channels/<int:channel_id>/stats/scenarios/<int:page>/', view_func=channel_stats_scenarios_view)
