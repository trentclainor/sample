# -*- coding: utf-8 -*-
import re
from flask import current_app
from datetime import datetime, timedelta
from wtforms import SubmitField, SelectField, HiddenField
from wtforms.validators import Optional
from flask.ext.login import current_user
from flask.ext.wtf import Form
from wtforms_html5 import TextField
from flask.ext.babel import gettext as _
from ..dictionary import *
from ..models import User, Channel, Scenario


class ConversionsFilterForm(Form):
    ip_range = TextField(_(u'Диапозон ip-адресов'), validators=[Optional()], description=u'например, 127.0.0.1/32')
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    client_status = SelectField(_(u'Статус клиента'), validators=[Optional()], coerce=str)
    scenario = SelectField(_(u'Клиент:сценарий'), validators=[Optional()], coerce=int)
    scenario_status = SelectField(_(u'Статус сценария'), validators=[Optional()], coerce=str)
    partner = SelectField(_(u'Партнер'), validators=[Optional()], coerce=int)
    partner_status = SelectField(_(u'Статус партнера'), validators=[Optional()], coerce=str)
    channel = SelectField(_(u'Партнер:канал'), validators=[Optional()], coerce=int)
    channel_status = SelectField(_(u'Статус канала'), validators=[Optional()], coerce=str)
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', CLICK_FILTER_STATUSES[0][0])
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        status = STATUSES_BLOCKED
        if current_user.is_admin():
            status = STATUSES
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(ConversionsFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        clients = User.query\
            .filter(User.role == 'client')\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        self.client_status.choices = ANY_STATUS + status
        partners = User.query\
            .filter(User.role == 'partner')\
            .order_by(User.name)
        self.partner.choices = ANY_PARTNER + [(c.id, c) for c in partners]
        self.partner_status.choices = ANY_STATUS + status
        scenarios = Scenario.query\
            .filter(Scenario.status == 'active')\
            .order_by(Scenario.name)
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.client.name + ' : ' + c.name) for c in scenarios]
        self.scenario_status.choices = ANY_STATUS + status
        channels = Channel.query\
            .filter(Channel.status == 'active')\
            .order_by(Channel.name)
        self.channel.choices = ANY_CHANNEL + [(c.id, c.partner.name + ' : ' + c.name) for c in channels]
        self.channel_status.choices = ANY_STATUS + status
        self.status.choices = ANY_STATUS + CONVERSATION_FILTER_STATUSES

    def validate(self):
        validate = Form.validate(self)
        if self.link.data:
            try:
                re.compile(self.link.data)
            except re.error as details:
                self.link.errors.append(details)
                validate = False
        return validate
