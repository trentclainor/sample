# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from flask import request, current_app
from wtforms import SubmitField, SelectField, TextField, FieldList, StringField, IntegerField, FormField, BooleanField, HiddenField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, URL
from wtforms import widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.templating import render_template_string
from flask.ext.wtf import Form
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..models import User, Scenario, Section, ScenarioSection, CodeTemplate, Parameter, Channel, Link
from ..stats.forms import StatsScenariosFilterForm, StatsDaysFilterForm, StatsPartnersFilterForm, StatsChannelsFilterForm
from ..extensions import db
from ..dictionary import *


def get_clients():
    return User.query.filter_by(role='client', status='active').order_by('name')


def get_scenarios():
    return Scenario.query.filter(Scenario.status == 'active').order_by(Scenario.name)


def get_scenario_sections(client_id, scenario):
    return Scenario.query.filter_by(status='active').order_by('name')


def get_templates():
    return CodeTemplate.query.order_by('name')


class ChooseClientsForm(Form):
    client = QuerySelectField(_(u'Выберите клиента'), validators=[DataRequired(message=_(u'Обязательное поле'))], query_factory=get_clients, allow_blank=True, blank_text=_(u'Любой клиент'))
    submit = SubmitField(_(u'Продолжить'))

    def validate(self):
        return Form.validate(self)


class ClientCodeForm(Form):
    client = None
    template = QuerySelectField(_(u'Шаблон'), query_factory=get_templates, allow_blank=True, blank_text=_(u'Выберите шаблон'))
    code = TextAreaField(_(u'Код'))
    submit = SubmitField(_(u'Получить код'))

    def __init__(self, *args, **kwargs):
        super(ClientCodeForm, self).__init__(*args, **kwargs)
        self.client = kwargs.get('obj', None)
        if self.template.data:
            self.code.data = self.template.data.template
        else:
            self.code.data = Parameter.get_by_key('default_template').value
        self.code.data = self.code.data.replace('${client_id}', unicode(self.client.get_id()))
        self.code.data = render_template_string(self.code.data)

    def validate(self):
        return False


class SectionFilterForm(Form):
    scenario = SelectField(_(u'Сценарий'), validators=[Optional()], coerce=int)
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(SectionFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_DELETED
        self.status.choices = ANY_STATUS + status
        self.scenario.choices = ANY_SCENARIO + [(c.id, c) for c in Scenario.query.filter(Scenario.client_id == kwargs.get('client_id')).order_by('name')]

    def validate(self):
        return Form.validate(self)


class SectionForm(Form):
    client = None
    section = None
    name = TextField(_(u'Название'), validators=[DataRequired(message=_(u'Обязательное поле'))])
    alias = TextField(_(u'Алиас'), validators=[DataRequired(message=_(u'Обязательное поле'))], description=u'только  латинские буквы, цифры, символ подчеркивания, точка, минус')
    section_type = SelectField(_(u'Тип'), validators=[DataRequired(message=_(u'Обязательное поле'))], coerce=str)
    wildcard = TextField(_(u'Шаблон'), validators=[DataRequired(message=_(u'Обязательное поле'))], description=u'регулярное выражение')

    def __init__(self, *args, **kwargs):
        self.section = kwargs.get('obj', None)
        super(SectionForm, self).__init__(*args, **kwargs)
        self.section_type.choices = CHOOSE_SECTION_TYPE + SECTION_TYPES
        if kwargs.get('client') and isinstance(kwargs.get('client'), User):
            self.client = kwargs.get('client')

    def validate(self):
        validate = Form.validate(self)
        try:
            re.compile(self.wildcard.data)
        except re.error as details:
            self.wildcard.errors.append(details)
            validate = False
        if self.section:
            client_id = self.section.client_id
        else:
            client_id = self.client.get_id()
        section = None
        if not self.section or (self.section and self.section.alias != self.alias.data):
            section = Section.query.filter_by(client_id=client_id, alias=self.alias.data).first()
        if section:
            self.alias.errors.append(_(u'Этот алиас используется у клиента'))
            validate = False
        return validate


class SectionCreateForm(SectionForm):
    submit = SubmitField(_(u'Добавить'))


class SectionEditForm(SectionForm):
    client = None
    submit = SubmitField(_(u'Сохранить'))


class SectionCodeForm(Form):
    section = None
    template = QuerySelectField(_(u'Шаблон'), query_factory=get_templates, allow_blank=True, blank_text=_(u'Выберите шаблон'))
    code = TextAreaField(_(u'Код раздела'))
    submit = SubmitField(_(u'Получить код'))

    def __init__(self, *args, **kwargs):
        super(SectionCodeForm, self).__init__(*args, **kwargs)
        self.section = kwargs.get('obj', None)
        if self.template.data:
            self.code.data = self.template.data.template
        else:
            self.code.data = Parameter.get_by_key('default_template').value
        self.code.data = self.code.data.replace('${client_id}', unicode(self.section.client_id))
        self.code.data = self.code.data.replace('${alias}', self.section.alias)
        self.code.data = render_template_string(self.code.data, alias=1)

    def validate(self):
        return False


class ScenarioFilterForm(Form):
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

    def validate(self):
        return Form.validate(self)


class ScenarioSectionForm(Form):
    section_id = HiddenField()
    checked = BooleanField(_(u'Раздел'), widget=widgets.CheckboxInput())
    count = IntegerField(_(u'Посещений разделов'), default=1, validators=[NumberRange(min=0, message=_(u'Укажите кол-во посещений раздела'))], description=_(u'минимальное количество посещений раздела, целое число от 0'))
    name = StringField(_(u'Название'), widget=widgets.HiddenInput())


class ScenarioForm(Form):
    client = None
    scenario = None
    name = TextField(_(u'Название'), validators=[DataRequired(message=_(u'Обязательное поле'))])
    cost_type = SelectField(_(u'Cпособ оплаты'), validators=[DataRequired(message=_(u'Обязательное поле'))], coerce=unicode)
    price = DecimalField(_(u'Цена'), validators=[DataRequired(message=_(u'Обязательное поле')), NumberRange(min=0, message=_(u'Укажите число больше 0.01'))], description=_(u'Стоимость за единицу (CPC, CPA)\nДесятичное число, например, 1.23 или 2 '))
    moderation = SelectField(_(u'Модерация'), validators=[DataRequired(message=_(u'Обязательное поле'))])
    section_list = FieldList(FormField(ScenarioSectionForm), _(u'Разделы'), validators=[DataRequired(message=_(u'Обязательное поле'))], widget=widgets.ListWidget(), description=_(u'минимальное количество посещений конктретного раздела'))
    total_count = IntegerField(_(u'Посещений разделов'), default=0, validators=[NumberRange(min=0, message=_(u'Укажите кол-во посещений разделов'))], description=_(u'Минимальное количество посещений разделов из списка, целое число от 0.\nЕсли 0, то укажите у конкретного раздела'))
    count_unique = BooleanField(_(u'Посещенные разделы уникальны'), default=0)

    def __init__(self, *args, **kwargs):
        super(ScenarioForm, self).__init__(*args, **kwargs)
        self.scenario = kwargs.get('obj', None)
        if self.scenario:
            self.client = self.scenario.client
        elif kwargs.get('client'):
            self.client = kwargs.get('client')
        self.cost_type.choices = CHOOSE_COST_TYPE + COST_TYPES
        self.moderation.choices = CHOOSE_MODERATION + MODERATION
        if not self.section_list:
            if self.scenario:
                q = Section.query.with_entities(Section, ScenarioSection.count).outerjoin(
                    ScenarioSection,
                    db.and_(
                        ScenarioSection.scenario_id == self.scenario.get_id(),
                        ScenarioSection.section_id == Section.id,
                    )).filter(Section.status == 'active').filter(Section.client_id == self.scenario.client_id).order_by(Section.name).group_by(Section.id)
                for section, count in q:
                    checked = 1
                    if count is None:
                        checked = 0
                        count = 0
                    self.section_list.append_entry({'section_id': section.get_id(), 'name': section.name, 'count': count, 'checked': checked})
            else:
                for section in self.client.sections:
                    if not section.is_active():
                        continue
                    self.section_list.append_entry({'section_id': section.get_id(), 'name': section.name, 'count': 1, 'checked': 0})

    def validate(self):
        validate = Form.validate(self)
        found = 0
        cnt = 0
        for section in self.section_list:
            if section.checked.data:
                found += 1
            if section.checked.data and section.count.data:
                cnt += 1
        if not found:
            validate = False
            self.section_list.errors.append(_(u'Выберите раздел выберите хотябы 1 раздел'))
        if cnt != found and not self.total_count.data:
            validate = False
            self.section_list.errors.append(_(u'Выбранные разделы должны содержать кол-во посещений отличным от 0'))
        elif not cnt and self.total_count.data > 0:
            validate = False
            self.total_count.errors.append(_(u'Укажите минимальное количество посещений разделов'))
        return validate


class ScenarioCreateForm(ScenarioForm):
    submit = SubmitField(_(u'Добавить'))


class ScenarioEditForm(ScenarioForm):
    submit = SubmitField(_(u'Сохранить'))


class ChannelFilterForm(Form):
    scenario = SelectField(_(u'Сценарий'), validators=[Optional()], coerce=int)
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(ChannelFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_BLOCKED
        if current_user.is_admin():
            status = STATUSES
        self.status.choices = ANY_STATUS + status
        self.scenario.choices = ANY_SCENARIO + [(c.id, c) for c in Scenario.query.filter(Scenario.client_id == kwargs.get('client_id')).order_by('name')]

    def validate(self):
        return Form.validate(self)


class PartnerFilterForm(Form):
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(PartnerFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_BLOCKED
        if current_user.is_admin():
            status = STATUSES
        self.status.choices = ANY_STATUS + status

    def validate(self):
        return Form.validate(self)


class ChannelCreateFilterForm(Form):
    scenario = HiddenField(validators=[NumberRange(min=0)])
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(ChannelCreateFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_BLOCKED
        if current_user.is_admin():
            status = STATUSES
        self.status.choices = ANY_STATUS + status

    def validate(self):
        return Form.validate(self)


class LinkForm(Form):
    channel_id = HiddenField()
    checked = BooleanField(_(u'Раздел'), widget=widgets.CheckboxInput())
    name = StringField(_(u'Каналы'), widget=widgets.HiddenInput())


class ChooseScenarioForm(Form):
    scenario = SelectField(_(u'Сценарий'), validators=[DataRequired(message=_(u'Обязательное поле'))], coerce=int)
    submit = SubmitField(_(u'Продолжить'))

    def __init__(self, *args, **kwargs):
        super(ChooseScenarioForm, self).__init__(*args, **kwargs)
        self.scenario.choices = ANY_SCENARIO + [(c.id, c) for c in Scenario.query.filter(Scenario.client_id == kwargs.get('client_id')).order_by('name')]

    def validate(self):
        return Form.validate(self)


class ChannelForm(Form):
    client = None
    scenario = None
    channels = FieldList(FormField(LinkForm), _(u'Каналы'), validators=[DataRequired(message=_(u'Обязательное поле'))], widget=widgets.ListWidget())

    def __init__(self, *args, **kwargs):
        super(ChannelForm, self).__init__(*args, **kwargs)
        self.scenario = kwargs.get('scenario', None)
        query = request.args.get('query')
        if self.scenario:
            self.client = self.scenario.client
        if kwargs.get('client'):
            self.client = kwargs.get('client')
        if not self.channels:
            q = Channel.query.with_entities(Channel)\
                .join(User, db.and_(User.id == Channel.partner_id))\
                .outerjoin(Link, db.and_(Link.channel_id == Channel.id, Link.scenario_id == self.scenario.get_id()))\
                .filter(Link.alias == None)\
                .group_by(Channel.id)
            if query:
                q = q.filter(db.or_(
                    Channel.name.like('%' + query + '%'),
                    Channel.url.like('%' + query + '%'),
                    User.name.like('%' + query + '%'),
                    User.email.like('%' + query + '%'),
                    User.company.like('%' + query + '%'),
                    User.contact_name.like('%' + query + '%'),
                    User.phone.like('%' + query + '%'),
                    User.address.like('%' + query + '%'),
                ))
            for channel in q:
                self.channels.append_entry({'channel_id': channel.get_id(), 'name': (u'%s : %s') % (channel.partner.name, channel.name), 'checked': 0})


class ChannelCreateForm(ChannelForm):
    # scenario = HiddenField()
    submit = SubmitField(_(u'Добавить'))


class ChanneEditForm(ChannelForm):
    submit = SubmitField(_(u'Сохранить'))


class LinkUrlForm(Form):
    link = None
    scenario = HiddenField()
    url = TextAreaField(_(u'Ссылка перехода'))

    def __init__(self, *args, **kwargs):
        super(LinkUrlForm, self).__init__(*args, **kwargs)
        self.link = kwargs.get('obj', None)
        self.url.data = self.url.data.replace('${click_id}', self.link.alias)

    def validate(self):
        validate = Form.validate(self)
        return validate


class LinkEditForm(Form):
    channel = None
    url = TextAreaField(_(u'Адрес перехода'), validators=[DataRequired(message=_(u'Обязательное поле')), URL(require_tld=False, message=_(u'укажите правильную ссылку'))], description=_(u'Включая http:// и можее содержать макрос ${click_id}'))
    submit = SubmitField(_(u'Сохранить'))

    def __init__(self, *args, **kwargs):
        super(LinkEditForm, self).__init__(*args, **kwargs)
        self.link = kwargs.get('obj', None)

    def validate(self):
        validate = Form.validate(self)
        # if not "${click_id}" in self.url.data:
        #     self.url.errors.append(_(u'Адрес перехода обязан содержать ${click_id}'))
        #     validate = False
        return validate


class ClientStatsDaysFilterForm(StatsDaysFilterForm):

    def __init__(self, *args, **kwargs):
        super(ClientStatsDaysFilterForm, self).__init__(*args, **kwargs)
        del self.client


class ClientStatsScenariosFilterForm(StatsScenariosFilterForm):

    def __init__(self, *args, **kwargs):
        super(ClientStatsScenariosFilterForm, self).__init__(*args, **kwargs)
        del self.client


class ClientStatsPartnersFilterForm(StatsPartnersFilterForm):

    def __init__(self, *args, **kwargs):
        super(ClientStatsPartnersFilterForm, self).__init__(*args, **kwargs)
        del self.client


class ClientStatsChannelsFilterForm(StatsChannelsFilterForm):

    def __init__(self, *args, **kwargs):
        super(ClientStatsChannelsFilterForm, self).__init__(*args, **kwargs)
        del self.client


class ScenarioStatsDaysFilterForm(StatsDaysFilterForm):

    def __init__(self, *args, **kwargs):
        super(ScenarioStatsDaysFilterForm, self).__init__(*args, **kwargs)
        del self.client
        del self.scenario


class ScenarioStatsPartnersFilterForm(StatsPartnersFilterForm):

    def __init__(self, *args, **kwargs):
        super(ScenarioStatsPartnersFilterForm, self).__init__(*args, **kwargs)
        del self.client
        del self.scenario


class ScenarioStatsChannelsFilterForm(StatsChannelsFilterForm):

    def __init__(self, *args, **kwargs):
        super(ScenarioStatsChannelsFilterForm, self).__init__(*args, **kwargs)
        del self.client
        del self.scenario
