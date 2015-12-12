# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from flask import url_for
from wtforms import SubmitField, SelectField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets import PasswordInput
from flask.ext.wtf import Form, RecaptchaField
from wtforms_html5 import TextField, EmailField
from flask.ext.wtf.recaptcha.validators import Recaptcha
from webapp.models import User
from webapp.forms import RedirectForm
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
from webapp.dictionary import *


class AuthResetForm(Form):
    user = None
    passwd = TextField(_(u'Новый пароль'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов'))], widget=PasswordInput(hide_value=False))
    confirm = PasswordField(_(u'Повтор пароля'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов')), EqualTo('passwd', message=_(u'Пароли не совпадают'))], widget=PasswordInput(hide_value=False))
    captcha = RecaptchaField(_(u'Введите текст'), validators=[Recaptcha(message=_(u'Введите символы'))])
    submit = SubmitField(_(u'Установить'))


class ForgotForm(Form):
    user = None
    email = EmailField(_(u'E-mail'), validators=[DataRequired(message=_(u'Обязательное поле')), Email(message=u'Укажите верный e-mail'), Length(min=6, max=64, message=u'от 4 до 64 символов')])
    submit = SubmitField(_(u'Восстановить'))

    def validate(self):
        validate = Form.validate(self)
        if not validate:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append(_(u'E-mail не найден'))
            return False
        self.user = user
        return True


class SigninForm(RedirectForm):
    user = None
    email = EmailField(_(u'E-mail'), validators=[DataRequired(message=_(u'Обязательное поле')), Email(message=_(u'Укажите верный e-mail')), Length(min=6, max=64, message=u'от 4 до 64 символов')])
    passwd = PasswordField(_(u'Пароль'), validators=[DataRequired(message=_(u'Обязательное поле'))], description=u'Введите пароль', widget=PasswordInput(hide_value=False))
    remember = BooleanField(_(u'Запомнить'), default=True)
    submit = SubmitField(_(u'Авторизироваться'))

    def validate(self):
        Form.validate(self)
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append(_(u'E-mail не найден'))
            return False
        if not user.is_active():
            self.email.errors.append(_(u'Ваш аккаунт заблокирован, да поможет вам ') + '<a href="' + url_for('feedback.index') + "?email=" + self.email.data + '">' + _(u'Служба поддержки') + '</a>')
            return False
        if not user.check_password(self.passwd.data):
            self.passwd.errors.append(_(u'Укажите правильный пароль, ') + '<a href="' + url_for('account.forgot') + "?email=" + self.email.data + u'">' + _(u'Забыли пароль?') + '</a>')
            return False
        self.user = user
        return True


class SignupForm(RedirectForm):
    user = None
    role = SelectField(_(u'Роль'), coerce=str, validators=[DataRequired(message=_(u'Обязательное поле'))])
    name = TextField(_(u'Имя'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=3, max=32, message=_(u'от 3 до 32 символов'))], description=u'русские или английские буквы')
    email = EmailField(_(u'E-mail'), validators=[DataRequired(message=_(u'Обязательное поле')), Email(message=_(u'Укажите верный e-mail')), Length(min=6, max=64, message=_(u'от 6 до 64 символов'))])
    passwd = TextField(_(u'Пароль'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов'))], widget=PasswordInput(hide_value=False))
    confirm = PasswordField(_(u'Повтор пароля'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов')), EqualTo('passwd', message=_(u'Пароли не совпадают'))], widget=PasswordInput(hide_value=False))
    captcha = RecaptchaField(_(u'Введите текст'), validators=[Recaptcha(message=_(u'Введите символы'))])
    accept = BooleanField(_(u'Согласен с <a href="/terms/" target="_blank">условиями</a>'), validators=[DataRequired(message=_(u'Вы не можете продолжить регистрацию, без согласия с нашими условиями'))], default=False)
    submit = SubmitField(_(u'Зарегистрироваться'))

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('role', '')
        super(SignupForm, self).__init__(*args, **kwargs)
        self.role.choices = [('', _(u'Выберите роль'))] + SIGNUP_ROLES

    def validate(self):
        validate = Form.validate(self)
        if not validate:
            return False
        user = User.query.filter_by(mail=self.email.data).first()
        if user:
            self.email.errors.append(_(u'Это e-mail используется в системе, ') + '<a href="' + url_for('account.forgot') + "?mail=" + self.email.data + u'">' + _(u'Забыли пароль?') + '</a>')
            validate = False
        if self.role.data not in dict(SIGNUP_ROLES):
            self.role.errors.append(_(u'Выберите роль из списка'))
            validate = False
        if not validate:
            return False
        return True


class SettingsForm(Form):
    name = TextField(_(u'Название'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=1, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    company = TextField(_(u'Компания'), validators=[Length(min=0, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    contact_name = TextField(_(u'Имя'), validators=[Length(min=0, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    phone = TextField(_(u'Телефон'), validators=[Length(min=0, max=64, message=_(u'от 1 до 64 символов'))], description=u'русские или английские буквы')
    address = TextAreaField(_(u'Адрес'))
    comment = TextAreaField(_(u'Коментарии'))
    submit = SubmitField(_(u'Сохранить'))


class SettingsEmailChangeForm(Form):
    current_passwd = PasswordField(_(u'Текущий пароль'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов'))], widget=PasswordInput(hide_value=False))
    new_mail = EmailField(_(u'Новый e-mail'), validators=[DataRequired(message=_(u'Обязательное поле')), Email(message=_(u'Укажите верный E-mail')), Length(min=6, max=64, message=_(u'от 6 до 64 символов'))])
    submit = SubmitField(_(u'Сменить e-mail'))

    def validate(self):
        validate = Form.validate(self)
        user = User.query.filter_by(email=self.new_mail.data).first()
        if user:
            self.new_mail.errors.append(_(u'Это e-mail используется в системе, ') + '<a href="' + url_for('account.forgot') + "?email=" + self.new_mail.data + u'">' + _(u'Забыли пароль?') + '</a>')
            validate = False
        if not current_user.check_password(self.current_passwd.data):
            self.current_passwd.errors.append(_(u'Неверно указан текущий пароль'))
            return False
        if not validate:
            return False
        return True


class SettingsNotificationForm(RedirectForm):
    user = None
    news = BooleanField(_(u'Получать новости'), validators=[Optional()])
    notice = BooleanField(_(u'Получать уведомления'), validators=[Optional()])
    submit = SubmitField(_(u'Сохранить'))


class SettingsPasswordForm(Form):
    current_passwd = PasswordField(_(u'Текущий пароль'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов'))], widget=PasswordInput(hide_value=False))
    passwd = PasswordField(_(u'Новый пароль'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов'))], widget=PasswordInput(hide_value=False))
    confirm = PasswordField(_(u'Повтор пароля'), validators=[DataRequired(message=_(u'Обязательное поле')), Length(min=6, message=_(u'не менее 6 символов')), EqualTo('passwd', message=_(u'Пароли не совпадают'))], widget=PasswordInput(hide_value=False))
    submit = SubmitField(_(u'Сменить пароль'))

    def validate(self):
        validate = Form.validate(self)
        if not current_user.check_password(self.current_passwd.data):
            self.current_passwd.errors.append(_(u'Неверно указан текущий пароль'))
            return False
        if not validate:
            return False
        return True
