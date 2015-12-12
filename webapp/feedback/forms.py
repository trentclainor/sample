# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from wtforms import Form, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms_html5 import TextField, EmailField
from flask.ext.wtf import Form, RecaptchaField
from flask.ext.wtf.recaptcha.validators import Recaptcha
from flask.ext.babel import gettext as _


class FeedbackUserForm(Form):
    text = TextAreaField(_(u'Текст сообщения'), validators=[DataRequired(message=_(u'введите текст сообщениия'))])
    submit = SubmitField(_(u'Отправить'))


class FeedbackAnonymousForm(Form):
    email = EmailField(_(u'Email'), validators=[DataRequired(message=_(u'Укажите Email')), Email(message=_(u'Укажите верный Email')), Length(min=6, max=64, message=_(u'от 6 до 64 символов'))])
    name = TextField(_(u'Имя'), validators=[DataRequired(message=_(u'Укажите имя')), Length(min=3, max=32, message=_(u'от 3 до 64 символов'))])
    text = TextAreaField(_(u'Текст сообщения'), validators=[DataRequired(message=_(u'Обязательное поле'))])
    captcha = RecaptchaField(_(u'Введите текст'), validators=[DataRequired(message=_(u'Обязательное поле')), Recaptcha(message=_(u'Введите символы'))])
    submit = SubmitField(_(u'Отправить'))
