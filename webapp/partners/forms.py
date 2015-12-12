# -*- coding: utf-8 -*-
from wtforms import SubmitField, SelectField, TextField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, URL
from flask.ext.wtf import Form
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..models import User, Channel, Scenario, Link, Parameter
from ..stats.forms import StatsScenariosFilterForm, StatsDaysFilterForm, StatsClientsFilterForm, StatsChannelsFilterForm
from ..extensions import db
from ..dictionary import *
# from .. import exception


class ChannelFilterForm(Form):
    client = SelectField(_(u'Клиент'), validators=[Optional()], coerce=int)
    no_client = SelectField(_(u'Не клиент'), validators=[Optional()], coerce=int)
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(ChannelFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_DELETED
        self.status.choices = ANY_STATUS + status
        self.client.choices = ANY_CLIENT
        self.no_client.choices = ANY_CLIENT
        clients = User.query\
            .join(Scenario, Scenario.client_id == User.id)\
            .join(Link, Link.scenario_id == Scenario.id)\
            .join(Channel, db.and_(Channel.id == Link.channel_id, Channel.partner_id == kwargs.get('partner_id')))\
            .order_by(User.name)
        self.client.choices = ANY_CLIENT + [(c.id, c) for c in clients]
        no_clients = [c.id for c in clients]
        self.no_client.choices = ANY_CLIENT + [(c.id, c) for c in User.query
            .filter(User.role == 'client', User.id.notin_(no_clients)).order_by(User.name).all()]

    def validate(self):
        return Form.validate(self)


class ChannelForm(Form):
    partner = None
    channel = None
    name = TextField(_(u'Название'), validators=[DataRequired(message=_(u'Обязательное поле'))])
    channel_type = SelectField(_(u'Модель выкупа'), validators=[DataRequired(message=_(u'Обязательное поле'))], coerce=str)
    url = TextAreaField(_(u'URL'), validators=[DataRequired(message=_(u'Обязательное поле')), URL(require_tld=False, message=_(u'укажите правильную ссылку'))], description=_(u'Включая http://'))
    price = DecimalField(_(u'Цена'), validators=[Optional(), NumberRange(min=0, message=_(u'Укажите число больше 0.01'))], description=_(u'Десятичное число, например, 1.23 или 2 '))

    def __init__(self, *args, **kwargs):
        self.channel = kwargs.get('obj', None)
        super(ChannelForm, self).__init__(*args, **kwargs)
        self.channel_type.choices = CHOOSE_CHANNEL_TYPE + CHANNEL_TYPES
        if kwargs.get('partner') and isinstance(kwargs.get('partner'), User):
            self.partner = kwargs.get('partner').get_id()

    def validate(self):
        validate = Form.validate(self)
        channel = None
        if not self.channel or (self.channel and self.channel.name != self.name.data):
            channel = Channel.query.filter_by(name=self.name.data).first()
        if channel:
            self.name.errors.append(_(u'Имя канала уже используется'))
            validate = False
        if self.channel_type.data == 'manually':
            self.price.data = 0
        elif self.channel_type.data and not self.price.data:
            self.price.errors.append(_(u'Укажите цену для этого типа канала'))
            validate = False
        return validate


class ChannelCreateForm(ChannelForm):
    submit = SubmitField(_(u'Добавить'))


class ChannelEditForm(ChannelForm):
    partner = None
    submit = SubmitField(_(u'Сохранить'))


class ClientFilterForm(Form):
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(ClientFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_BLOCKED
        if current_user.is_admin():
            status = STATUSES
        self.status.choices = ANY_STATUS + status

    def validate(self):
        return Form.validate(self)


class ScenarioFilterForm(Form):
    channel = SelectField(_(u'Канал'), validators=[Optional()], coerce=int)
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(ScenarioFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_BLOCKED
        if current_user.is_admin():
            status = STATUSES
        self.status.choices = ANY_STATUS + status
        self.channel.choices = ANY_SCENARIO + [(c.id, c) for c in Channel.query.filter(Channel.partner_id == kwargs.get('partner_id')).order_by('name')]

    def validate(self):
        return Form.validate(self)


class LinkUrlForm(Form):
    link = None
    url = TextAreaField(_(u'Ссылка перехода'))

    def __init__(self, *args, **kwargs):
        super(LinkUrlForm, self).__init__(*args, **kwargs)
        self.link = kwargs.get('obj', None)
        self.url.data = Parameter.get_by_key('click_url').value
        self.url.data = self.url.data.replace('${click_id}', self.link.alias)

    def validate(self):
        validate = Form.validate(self)
        return validate


class PartnerStatsDaysFilterForm(StatsDaysFilterForm):

    def __init__(self, *args, **kwargs):
        super(PartnerStatsDaysFilterForm, self).__init__(*args, **kwargs)
        del self.partner


class PartnerStatsClientsFilterForm(StatsClientsFilterForm):

    def __init__(self, *args, **kwargs):
        super(PartnerStatsClientsFilterForm, self).__init__(*args, **kwargs)
        del self.partner


class PartnerStatsChannelsFilterForm(StatsChannelsFilterForm):

    def __init__(self, *args, **kwargs):
        super(PartnerStatsChannelsFilterForm, self).__init__(*args, **kwargs)
        del self.partner


class ChannelStatsDaysFilterForm(StatsDaysFilterForm):

    def __init__(self, *args, **kwargs):
        super(ChannelStatsDaysFilterForm, self).__init__(*args, **kwargs)
        del self.partner
        del self.channel


class ChannelStatsClientsFilterForm(StatsDaysFilterForm):

    def __init__(self, *args, **kwargs):
        super(ChannelStatsClientsFilterForm, self).__init__(*args, **kwargs)
        del self.client
        del self.scenario
        del self.partner
        del self.channel


class ChannelStatsScenariosFilterForm(StatsScenariosFilterForm):

    def __init__(self, *args, **kwargs):
        super(ChannelStatsScenariosFilterForm, self).__init__(*args, **kwargs)
        del self.client
        del self.partner
        del self.channel
