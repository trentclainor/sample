# -*- coding: utf-8 -*-
from wtforms import SubmitField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask.ext.wtf import Form
from wtforms_html5 import TextField, EmailField, TelField
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..users.forms import UserForm, UserEditForm
from ..models import User, CodeTemplate
from ..widgets import MyPasswordInput
from ..dictionary import *
# from .. import exception


class UserDeleteForm(Form):
    pass


class FilterForm(Form):
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def validate(self):
        return Form.validate(self)


class UserAdminCreateForm(UserForm):
    role = SelectField(_(u'Роль'), validators=[Optional()], coerce=str)
    submit = SubmitField(_(u'Добавить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('role', '')
        super(UserAdminCreateForm, self).__init__(*args, **kwargs)
        self.role.choices = CHOOSE_ROLE + ADMIN_ROLES


class UserAdminEditForm(UserForm):
    passwd = None
    confirm = None
    role = SelectField(_(u'Роль'), validators=[Optional()], coerce=str)
    submit = SubmitField(_(u'Сохранить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('role', '')
        super(UserAdminEditForm, self).__init__(*args, **kwargs)
        self.role.choices = ADMIN_ROLES


class CodeTemplateForm(Form):
    code_temaplate = None
    name = TextField(_(u'Название'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=1, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    template = TextAreaField(_(u'Шаблон кода'), validators=[DataRequired(message=_(u'Обязательное поле'))], description=u'шаблон кода раздела обязан содержать ${alias} и ${client_id}')
    template_static = TextAreaField(_(u'Шаблон статической части'))

    def __init__(self, *args, **kwargs):
        self.code_template = kwargs.get('obj', None)
        super(CodeTemplateForm, self).__init__(*args, **kwargs)

    def validate(self):
        validate = Form.validate(self)
        if not "${alias}" in self.template.data or not "${client_id}" in self.template.data:
            self.template.errors.append(_(u'Шаблон кода обязан содержать ${alias} и ${client_id}'))
            validate = False
        if not self.code_template or self.code_template.name != self.name.data:
            code_temaplate = CodeTemplate.query.filter_by(name=self.name.data).first()
            if code_temaplate:
                self.name.errors.append(_(u'Это название используется в системе'))
                validate = False
        return validate


class CodeTemplateCreateForm(CodeTemplateForm):
    submit = SubmitField(_(u'Добавить'))


class CodeTemplateEditForm(CodeTemplateForm):
    submit = SubmitField(_(u'Сохранить'))


class ParameterForm(Form):
    parameter = None
    name = TextField(_(u'Название'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=1, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    key = TextField(_(u'Ключ'), validators=[DataRequired(message=_(u'Обязательное поле'))])
    value = TextAreaField(_(u'Значение'), validators=[DataRequired(message=_(u'Обязательное поле'))])

    def __init__(self, *args, **kwargs):
        self.parameter = kwargs.get('obj', None)
        super(ParameterForm, self).__init__(*args, **kwargs)

    def validate(self):
        validate = Form.validate(self)
        return validate


class ParameterCreateForm(ParameterForm):
    submit = SubmitField(_(u'Добавить'))


class ParameterEditForm(ParameterForm):
    submit = SubmitField(_(u'Сохранить'))
