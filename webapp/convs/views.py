# -*- coding: utf-8 -*-
from netaddr import IPNetwork
from datetime import datetime, timedelta
from flask import flash, url_for, request, current_app, jsonify
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..decorators import roles_accepted
from ..dictionary import STATUSES_BLOCKED
from ..helpers import Pagination
from ..extensions import db
from .. import exception
from ..controller import BaseController
from ..models import ConversionsLog, ClicksLog, Scenario, Channel, User
from . import convs
from .forms import ConversionsFilterForm

STATUSES_BLOCKED = [k[0] for k in STATUSES_BLOCKED]


class ConversionsView(BaseController):
    template = 'convs.html'
    header = _(u'Просмотр списка конверсий')
    breadcrumbs = [(_(u'Просмотр списка конверсий'), '', {})]
    _messages = {
        'accepted': _(u'Конверсии успешно приняты'),
        'rejected': _(u'Конверсии успешно отклонены'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    @roles_accepted('manager', 'admin')
    def get(self, **extra):
        direction = request.args.get('dir', 'asc')
        sort = request.args.get('sort', 'id')
        conv_id = int(request.args.get('id', 0))
        client_id = int(request.args.get('client', 0))
        scenario_id = int(request.args.get('scenario', 0))
        partner_id = int(request.args.get('partner', 0))
        channel_id = int(request.args.get('channel', 0))
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        form = ConversionsFilterForm(request.args, csrf_enabled=False)
        ip_range = request.args.get('ip_range', None)
        client_status = request.args.get('client_status', None)
        scenario_status = request.args.get('scenario_status', None)
        partner_status = request.args.get('partner_status', None)
        channel_status = request.args.get('channel_status', None)
        status = form.status.data
        date_from = datetime.strptime(form.date_from.data + ' 00:00:00', current_app.config.get('DATE_FROM_FORMAT'))
        date_to = datetime.strptime(form.date_to.data + ' 23:59:59', current_app.config.get('DATE_TO_FORMAT'))
        partner = db.aliased(User)
        client = db.aliased(User)
        q = ConversionsLog.query.with_entities(
            ConversionsLog.id.label('id'),
            ConversionsLog.click_id,
            ConversionsLog.uid,
            ConversionsLog.ip,
            ConversionsLog.user_agent,
            ConversionsLog.referer,
            ConversionsLog.payout,
            ConversionsLog.cost,
            ConversionsLog.status,
            ConversionsLog.created,
            Channel.id.label('channel_id'),
            Channel.name.label('channel_name'),
            partner.id.label('partner_id'),
            partner.name.label('partner_name'),
            Scenario.id.label('scenario_id'),
            Scenario.name.label('scenario_name'),
            client.id.label('client_id'),
            client.name.label('client_name'),
            ClicksLog.status.label('click_status'),
        )\
        .join(Channel, db.and_(Channel.id == ConversionsLog.channel_id, Channel.status.in_(STATUSES_BLOCKED)))\
        .join(partner, db.and_(partner.id == Channel.partner_id, partner.status.in_(STATUSES_BLOCKED)))\
        .join(Scenario, db.and_(Scenario.id == ConversionsLog.scenario_id, Scenario.status.in_(STATUSES_BLOCKED)))\
        .join(client, db.and_(client.id == Scenario.client_id, client.status.in_(STATUSES_BLOCKED)))\
        .join(ClicksLog, ClicksLog.id == ConversionsLog.click_id)
        if conv_id:
            q = q.filter(ConversionsLog.id == conv_id)
        else:
            if date_from and date_to:
                q = q.filter(ConversionsLog.created.between(date_from, date_to))
            if client_id:
                q = q.filter(client.id == client_id)
            if client_status:
                q = q.filter(client.status == client_status)
            if scenario_id:
                q = q.filter(Scenario.id == scenario_id)
            if channel_status:
                q = q.filter(Scenario.status == scenario_status)
            if partner_id:
                q = q.filter(partner.id == partner_id)
            if partner_status:
                q = q.filter(partner.status == partner_status)
            if channel_id:
                q = q.filter(Channel.id == channel_id)
            if channel_status:
                q = q.filter(Channel.status == channel_status)
            if status:
                q = q.filter(ConversionsLog.status == status)
            if ip_range:
                ip_list = IPNetwork(ip_range)
                q = q.filter(db.func.inet_aton(ConversionsLog.ip).between(int(ip_list[0]), int(ip_list[-1])))
        sort, column_sorted = self.sortable(q, ConversionsLog, field=sort, default='id', direction=direction)
        q = q.order_by(column_sorted)
        convs = Pagination(q, extra.get('page', 1), ConversionsLog.per_page)
        return super(ConversionsView, self).get(form=form, default_sort=sort, default_dir=direction, convs=convs, **extra)

    @roles_accepted('manager', 'admin')
    def post(self, **extra):
        try:
            convs = request.form.getlist('conv_ids')
            action = request.form.get('action')
            status = None
            if action == 'accept':
                status = 'accepted'
            elif action == 'reject':
                status = 'rejected'
            if convs and status:
                ConversionsLog.query.filter(ConversionsLog.id.in_(convs)).update({'status': status}, synchronize_session='fetch')
                db.session.commit()
                flash(self._messages[status], 'success')
            return self.redirect(request.args.get("next", url_for("convs.index", **extra)))
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                flash(self._messages['internal_error'], 'error')
            db.session.rollback()
        return super(ConversionsView, self).post(**extra)


class ConversionAcceptView(BaseController):

    @roles_accepted('admin', 'manager')
    def post(self, **extra):
        try:
            conv = ConversionsLog.query.get_or_404(extra.get('id'))
            if not current_user.is_admin() and not conv.is_new():
                raise exception.AccessDenied()
            conv.accept()
        except exception.AccessDenied, e:
            db.session.rollback()
            return jsonify({'status': 0, 'msg': unicode(e)})
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
            db.session.rollback()
        return jsonify({'status': 1})


class ConversionRejectView(BaseController):

    @roles_accepted('admin', 'manager')
    def post(self, **extra):
        try:
            conv = ConversionsLog.query.get_or_404(extra.get('id'))
            if not current_user.is_admin() and not conv.is_new():
                raise exception.AccessDenied()
            conv.reject()
        except exception.AccessDenied, e:
            db.session.rollback()
            return jsonify({'status': 0, 'msg': unicode(e)})
        except Exception, e:
            db.session.rollback()
            if current_app.config['DEBUG']:
                raise e
            else:
                return jsonify({'status': 0})
        return jsonify({'status': 1})


convs_view = ConversionsView.as_view('index')

convs.add_url_rule('/', defaults={'page': 1}, view_func=convs_view)
convs.add_url_rule('/<int:page>/', view_func=convs_view)

convs.add_url_rule('/accept/<int:id>/', view_func=ConversionAcceptView.as_view('accept'))
convs.add_url_rule('/reject/<int:id>/', view_func=ConversionRejectView.as_view('reject'))
