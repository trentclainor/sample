# -*- coding: utf-8 -*-
from flask import current_app
from datetime import datetime, timedelta
from wtforms import SubmitField, SelectField, HiddenField
from wtforms.validators import Optional
from flask.ext.login import current_user
from flask.ext.wtf import Form
from wtforms_html5 import TextField
from flask.ext.babel import gettext as _
from ..dictionary import *
from ..models import User, Channel, Scenario, ReportScenario, ReportChannel, ReportScenarioChannel
from ..extensions import db


class StatsDaysFilterForm(Form):
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    partner = SelectField(_(u'Партнер'), validators=[Optional()], coerce=int)
    scenario = SelectField(_(u'Клиент:сценарий'), validators=[Optional()], coerce=int)
    channel = SelectField(_(u'Партнер:канал'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(StatsDaysFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        clients = User.query\
            .join(Scenario, Scenario.client_id == User.id)\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .filter(User.role == 'client')\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        partners = User.query\
            .join(Channel, Channel.partner_id == User.id)\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .filter(User.role == 'partner')\
            .order_by(User.name)
        self.partner.choices = ANY_PARTNER + [(c.id, c) for c in partners]
        scenarios = Scenario.query\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .join(User, User.id == Scenario.client_id)\
            .order_by(User.name, Scenario.name)
        if self.client.data:
            scenarios = scenarios.filter(Scenario.client_id == self.client.data)
        if kwargs.get('client_id'):
            scenarios = scenarios.filter(Scenario.client_id == kwargs.get('client_id'))
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.client.name + ' : ' + c.name) for c in scenarios]
        channels = Channel.query\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .join(User, User.id == Channel.partner_id)\
            .order_by(User.name, Channel.name)
        if self.partner.data:
            channels = channels.filter(Channel.partner_id == self.partner.data)
        if kwargs.get('partner_id'):
            channels = channels.filter(Channel.partner_id == kwargs.get('partner_id'))
        self.channel.choices = ANY_CHANNEL + [(c.id, c.partner.name + ' : ' + c.name) for c in channels]


class StatsPartnersFilterForm(Form):
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    scenario = SelectField(_(u'Клиент:сценарий'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(StatsPartnersFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        clients = User.query\
            .filter(User.role == 'client')\
            .join(Scenario, Scenario.client_id == User.id)\
            .join(ReportScenario, db.and_(ReportScenario.scenario_id == Scenario.id))\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        scenarios = Scenario.query\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .join(User, User.id == Scenario.client_id)\
            .order_by(User.name, Scenario.name)
        if self.client.data:
            scenarios = scenarios.filter(Scenario.client_id == self.client.data)
        if kwargs.get('client_id'):
            scenarios = scenarios.filter(Scenario.client_id == kwargs.get('client_id'))
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.client.name + ' : ' + c.name) for c in scenarios]


class StatsChannelsFilterForm(Form):
    partner = SelectField(_(u'Партнер'), validators=[Optional()], coerce=int)
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    scenario = SelectField(_(u'Клиент:сценарий'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(StatsChannelsFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        partners = User.query\
            .join(Channel, Channel.partner_id == User.id)\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .filter(User.role == 'partner')\
            .order_by(User.name)
        self.partner.choices = ANY_PARTNER + [(c.id, c) for c in partners]
        clients = User.query\
            .join(Scenario, Scenario.client_id == User.id)\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .filter(User.role == 'client')\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        scenarios = Scenario.query\
            .join(User, User.id == Scenario.client_id)\
            .order_by(User.name, Scenario.name)
        if self.client.data:
            scenarios = scenarios.filter(Scenario.client_id == self.client.data)
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.client.name + ' : ' + c.name) for c in scenarios]


class StatsClientsFilterForm(Form):
    partner = SelectField(_(u'Партнер'), validators=[Optional()], coerce=int)
    channel = SelectField(_(u'Партнер:канал'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(StatsClientsFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        partners = User.query\
            .join(Channel, Channel.partner_id == User.id)\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .filter(User.role == 'partner')\
            .order_by(User.name)
        self.partner.choices = ANY_PARTNER + [(c.id, c) for c in partners]
        channels = Channel.query\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .join(User, User.id == Channel.partner_id)\
            .order_by(User.name, Channel.name)
        if self.partner.data:
            channels = channels.filter(Channel.partner_id == self.partner.data)
        if kwargs.get('partner_id'):
            channels = channels.filter(Channel.partner_id == kwargs.get('partner_id'))
        self.channel.choices = ANY_CHANNEL + [(c.id, c.partner.name + ' : ' + c.name) for c in channels]


class StatsScenariosFilterForm(Form):
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    partner = SelectField(_(u'Партнер'), validators=[Optional()], coerce=int)
    channel = SelectField(_(u'Партнер:канал'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(StatsScenariosFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        clients = User.query\
            .join(Scenario, Scenario.client_id == User.id)\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .filter(User.role == 'client')\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        partners = User.query\
            .join(Channel, Channel.partner_id == User.id)\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .filter(User.role == 'partner')\
            .order_by(User.name)
        self.partner.choices = ANY_PARTNER + [(c.id, c) for c in partners]
        channels = Channel.query\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .join(User, User.id == Channel.partner_id)\
            .order_by(User.name, Channel.name)
        if self.partner.data:
            channels = channels.filter(Channel.partner_id == self.partner.data)
        self.channel.choices = ANY_CHANNEL + [(c.id, c.partner.name + ' : ' + c.name) for c in channels]


class ClientStatsDaysFilterForm(Form):
    scenario = SelectField(_(u'Cценарий'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(ClientStatsDaysFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        scenarios = Scenario.query\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .order_by(Scenario.name)\
            .filter(Scenario.client_id == current_user.get_id())
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.name) for c in scenarios]


class ClientStatsPartnersFilterForm(Form):
    scenario = SelectField(_(u'Сценарий'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(ClientStatsPartnersFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        scenarios = Scenario.query\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .filter(Scenario.client_id == current_user.get_id())\
            .order_by(Scenario.name)
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.name) for c in scenarios]


class ClientStatsChannelsFilterForm(Form):
    scenario = SelectField(_(u'Сценарий'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(ClientStatsChannelsFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        scenarios = Scenario.query\
            .join(ReportScenario, ReportScenario.scenario_id == Scenario.id)\
            .filter(Scenario.client_id == current_user.get_id())\
            .order_by(Scenario.name)
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.name) for c in scenarios]


class ClientStatsScenariosFilterForm(Form):
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(ClientStatsScenariosFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))


class PartnerStatsDaysFilterForm(Form):
    channel = SelectField(_(u'Канал'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(PartnerStatsDaysFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        channels = Channel.query\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .filter(Channel.partner_id == current_user.get_id())\
            .order_by(Channel.name)
        self.channel.choices = ANY_CHANNEL + [(c.id, c.name) for c in channels]


class PartnerStatsChannelsFilterForm(Form):
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    scenario = SelectField(_(u'Клиент:сценарий'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(PartnerStatsChannelsFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        clients = User.query\
            .join(Scenario, Scenario.client_id == User.id)\
            .join(ReportScenarioChannel, db.and_(ReportScenarioChannel.scenario_id == Scenario.id))\
            .join(Channel, db.and_(ReportScenarioChannel.channel_id == Channel.id, Channel.partner_id == current_user.get_id()))\
            .filter(User.role == 'client')\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        scenarios = Scenario.query\
            .join(ReportScenarioChannel, ReportScenarioChannel.scenario_id == Scenario.id)\
            .join(Channel, db.and_(ReportScenarioChannel.channel_id == Channel.id, Channel.partner_id == current_user.get_id()))\
            .order_by(Scenario.name)
        self.scenario.choices = ANY_SCENARIO + [(c.id, c.name) for c in scenarios]


class PartnerStatsClientsFilterForm(Form):
    channel = SelectField(_(u'Канал'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(PartnerStatsClientsFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        channels = Channel.query\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .filter(Channel.partner_id == current_user.get_id())\
            .order_by(Channel.name)
        self.channel.choices = ANY_CHANNEL + [(c.id, c.name) for c in channels]


class PartnerStatsScenariosFilterForm(Form):
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    channel = SelectField(_(u'Канал'), validators=[Optional()], coerce=int)
    date_from = HiddenField()
    date_to = HiddenField()
    daterange = TextField(_(u'Период'), validators=[])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        date_to = datetime.today()
        month = timedelta(days=29)
        date_from = date_to - month
        kwargs.setdefault('date_from', date_from.strftime(current_app.config.get('DATE_FORMAT')))
        kwargs.setdefault('date_to', date_to.strftime(current_app.config.get('DATE_FORMAT')))
        super(PartnerStatsScenariosFilterForm, self).__init__(*args, **kwargs)
        if not self.date_from.data:
            self.date_from.data = date_from.strftime(current_app.config.get('DATE_FORMAT'))
        if not self.date_to.data:
            self.date_to.data = date_to.strftime(current_app.config.get('DATE_FORMAT'))
        clients = User.query\
            .join(Scenario, Scenario.client_id == User.id)\
            .join(ReportScenarioChannel, db.and_(ReportScenarioChannel.scenario_id == Scenario.id))\
            .join(Channel, db.and_(ReportScenarioChannel.channel_id == Channel.id, Channel.partner_id == current_user.get_id()))\
            .filter(User.role == 'client')\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        channels = Channel.query\
            .join(ReportChannel, ReportChannel.channel_id == Channel.id)\
            .filter(Channel.partner_id == current_user.get_id())\
            .order_by(Channel.name)
        self.channel.choices = ANY_CHANNEL + [(c.id, c.name) for c in channels]
