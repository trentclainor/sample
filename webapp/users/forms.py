# -*- coding: utf-8 -*-
from wtforms import SubmitField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask.ext.wtf import Form
from wtforms_html5 import TextField, EmailField, TelField
from flask.ext.babel import gettext as _
from flask.ext.login import current_user
from ..models import User
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


class UserFilterForm(Form):
    status = SelectField(_(u'Статус'), validators=[Optional()], coerce=str)
    query = TextField(_(u'Строка поиска'), validators=[Optional(), Length(max=100, message=_(u'до 100 символов'))])
    submit = SubmitField(_(u'Применить'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('status', '')
        super(UserFilterForm, self).__init__(*args, **kwargs)
        status = STATUSES_BLOCKED
        if current_user.is_admin():
            status = STATUSES
        self.status.choices = ANY_STATUS + status + [('end_money', _(u'Закончились деньги'))]

    def validate(self):
        return Form.validate(self)


class UserForm(Form):
    user = None
    role = None
    name = TextField(_(u'Название'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=1, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    email = EmailField(_(u'E-mail'), validators=[DataRequired(message=_(u'Обязательное поле')), Email(message=_(u'Укажите верный e-mail')), Length(min=6, max=64, message=_(u'от 6 до 64 символов'))])
    passwd = TextField(_(u'Пароль'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов'))], widget=MyPasswordInput())
    confirm = PasswordField(_(u'Повтор пароля'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов')), EqualTo('passwd', message=_(u'Пароли не совпадают'))], widget=MyPasswordInput())
    company = TextField(_(u'Компания'), validators=[Length(min=0, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    contact_name = TextField(_(u'Имя'), validators=[Length(min=0, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    phone = TelField(_(u'Телефон'), validators=[Length(min=0, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    address = TextAreaField(_(u'Адрес'))
    comment = TextAreaField(_(u'Коментарии'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('obj', None)
        super(UserForm, self).__init__(*args, **kwargs)

    def validate(self):
        validate = Form.validate(self)
        user = None
        if not self.user or (self.user and self.user.email != self.email.data):
            user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(_(u'Это e-mail используется в системе'))
            validate = False
        return validate


class UserCreateForm(UserForm):
    submit = SubmitField(_(u'Добавить'))


class UserEditForm(UserForm):
    passwd = None
    confirm = None
    submit = SubmitField(_(u'Сохранить'))

    def validate(self):
        validate = Form.validate(self)
        if self.user.email != self.email.data:
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                self.email.errors.append(_(u'Этот e-mail используется в системе'))
                validate = False
        return validate


class UserPasswordEditForm(Form):
    passwd = PasswordField(_(u'Новый пароль'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов'))], widget=MyPasswordInput())
    confirm = PasswordField(_(u'Повтор пароля'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов')), EqualTo('passwd', message=_(u'Пароли не совпадают'))], widget=MyPasswordInput())
    submit = SubmitField(_(u'Сменить пароль'))

    def validate(self):
        validate = Form.validate(self)
        if not validate:
            return False
        return True
