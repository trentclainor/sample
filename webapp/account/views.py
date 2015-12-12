# -*- coding: utf-8 -*-

from flask import flash, redirect, request, url_for, current_app
from flask.ext.login import current_user, login_required
from flask.ext.mail import Message
from flask.ext.babel import gettext as _
from ..extensions import db, mail
from .. import exception
from ..helpers import login_user, logout_user
from ..models import User
from ..controller import BaseController
from .forms import AuthResetForm, ForgotForm, SettingsForm, SigninForm, SignupForm, SettingsNotificationForm, SettingsPasswordForm, SettingsEmailChangeForm
from . import account


class AuthView(BaseController):
    _messages = {}

    def get(self, **extra):
        uid = int(extra.get('uid', 0))
        secret = extra.get('secret', None)
        try:
            user = User.get(uid)
            if not user:
                raise exception.Auth('User not found')
            if not user.check_secret(secret):
                raise exception.Auth('User wrong secret')
            if not login_user(user, remember=True):
                raise exception.Auth('User auth error')
        except Exception, e:
            if current_app.config['DEBUG']:
                raise e
            else:
                flash(self._messages['invalid_key'], 'danger')
            return self.redirect(extra.get('redirect', None))
        return super(AuthView, self).get(**extra)


class AuthResetView(AuthView):
    header = _(u'Установка нового пароля')
    breadcrumbs = [(_(u'Установка нового пароля'), '', {})]
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'Успешно изменили пароль'),
        'invalid_key': _(u'Ссылка восстановления пароля устарела, восстановите пароль еще раз'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def get(self, **extra):
        form = AuthResetForm(request.form)
        return super(AuthResetView, self).get(redirect=url_for("account.forgot"), form=form, **extra)

    @login_required
    def post(self, **extra):
        if not current_user.is_authenticated():
            raise exception.Auth('User auth error')
        form = AuthResetForm(request.form)
        if form.validate_on_submit():
            try:
                current_user.set_password(form.passwd.data)
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(request.args.get("next") or url_for("index.page"))
            except exception.Auth, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'danger')
                db.session.rollback()
        return super(AuthResetView, self).post(form=form, **extra)


class ForgotView(BaseController):
    header = _(u'Восстановление пароля')
    breadcrumbs = [(_(u'Восстановление пароля'), '', {})]
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'Вам отправлено письмо с инструкциями'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def get(self, **extra):
        form = ForgotForm()
        form.email.data = request.args.get('email')
        return super(ForgotView, self).get(form=form, **extra)

    def post(self, **extra):
        form = ForgotForm(request.form)
        if form.validate_on_submit():
            try:
                user = form.user
                user.set_secret()
                db.session.commit()
                msg = Message(_(u'Вы запросили восстановление пароля в системе Ледник.'), body=self.render(
                    template='mail/forgot.html',
                    role=user.get_role(),
                    user=user,
                    link=url_for('account.reset', uid=user.get_id(), secret=user.secret, _external=True)).encode("utf-8"),
                    recipients=[user.email],
                )
                mail(current_app).send(msg)
                flash(self._messages['success'], 'success')
                return self.redirect(url_for("index.page"))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'danger')
                db.session.rollback()
        return super(ForgotView, self).post(form=form, **extra)


class SigninView(BaseController):
    header = _(u'Авторизация')
    breadcrumbs = [(_(u'Авторизация'), '', {})]
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'Успешно авторизировались'),
        'invalid_auth': _(u'Ошибка авторизации'),
        'invalid_form': _(u'E-mail или пароль неверно указаны'),
    }

    def get(self, **extra):
        form = SigninForm()
        form.email.data = request.args.get('email')
        return super(SigninView, self).get(form=form, **extra)

    def post(self, **extra):
        form = SigninForm(request.form)
        if form.validate_on_submit():
            remember = request.form.get("remember", "no") == "yes"
            if login_user(form.user, remember=remember):
                flash(self._messages['success'], 'success')
                return redirect(request.args.get("next") or url_for("index.page"))
            else:
                flash(self._messages['invalid_auth'], 'danger')
        return super(SigninView, self).post(form=form, **extra)


class SignupView(BaseController):
    header = _(u'Регистрация')
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'Успешно зарегистрировались'),
        'invalid_auth': _(u'Ошибка при регистрации'),
        'invalid_form': _(u'Укажите правильные данные'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def get(self, **extra):
        form = SignupForm()
        form.email.data = request.args.get('email')
        return super(SignupView, self).get(form=form, **extra)

    def post(self, **extra):
        form = SignupForm(request.form)
        if form.validate_on_submit():
            referrer_id = 0
            if request.cookies.get('pid'):
                referrer_id = int(request.cookies.get('pid'))
            role = form.role.data
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.passwd.data,
                role=role,
                referrer_id=referrer_id,
            )
            db.session.add(user)
            db.session.commit()
            # db.session.flush()
            # db.session.refresh(user)
            # if role == 'client':
            #     client = Client(client_id=user.get_id())
            #     db.session.add(client)
            # elif role == 'partner':
            #     partner = Partner(partner_id=user.get_id())
            #     db.session.add(partner)
            # else:
            #     raise Exception("Role not found")
            if login_user(user):
                flash(self._messages['success'], 'success')
            msg = Message(_(u'Вы успешно зарегистрировались в системе Ледник.'), body=self.render(template='mail/registration.html', form=form).encode("utf-8"), recipients=[user.email], charset="UTF-8")
            mail(current_app).send(msg)
            return self.redirect(request.args.get("next", url_for("index.page")))
        return super(SignupView, self).post(form=form, **extra)


class SettingsView(BaseController):
    header = _(u'Редактирование профиля')
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'Настройки успешно сохранены'),
        'invalid_form': _(u'Укажите правильные данные'),
        'internal_error': _(u'Внутренняя ошибка'),
    }
    decorators = [login_required]

    def get(self, **extra):
        return super(SettingsView, self).get(form=SettingsForm(obj=current_user), **extra)

    def post(self, **extra):
        form = SettingsForm(request.form)
        if form.validate_on_submit():
            form.populate_obj(current_user)
            try:
                current_user.update(
                    name=form.name.data,
                    company=form.company.data,
                    contact_name=form.contact_name.data,
                    phone=form.phone.data,
                    address=form.address.data,
                    comment=form.comment.data,
                )
                flash(self._messages['success'], 'success')
                return redirect(url_for("account.settings"))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'danger')
                db.session.rollback()
        return super(SettingsView, self).post(form=form, **extra)


class SettingsNotificationView(BaseController):
    header = _(u'Настройка уведомлений')
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'Уведомления успешно изменены'),
        'internal_error': _(u'Внутренняя ошибка'),
    }
    decorators = [login_required]

    def get(self, **extra):
        return super(SettingsNotificationView, self).get(form=SettingsNotificationForm(obj=current_user), **extra)

    def post(self, **extra):
        form = SettingsNotificationForm(request.form)
        if form.validate_on_submit():
            form.populate_obj(current_user)
            try:
                current_user.update(news=form.news.data, notice=form.notice.data)
                flash(self._messages['success'], 'success')
                return redirect(url_for("account.settings.notification"))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'danger')
                db.session.rollback()
        return super(SettingsNotificationView, self).post(form=form, **extra)


class SettingsPasswordView(BaseController):
    header = _(u'Изменение пароля')
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'Пароль успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }
    decorators = [login_required]

    def get(self, **extra):
        return super(SettingsPasswordView, self).get(form=SettingsPasswordForm(), **extra)

    def post(self, **extra):
        form = SettingsPasswordForm(request.form)
        if form.validate_on_submit():
            form.populate_obj(current_user)
            try:
                current_user.update(password=form.passwd.data)
                flash(self._messages['success'], 'success')
                return redirect(url_for("account.settings.password"))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'danger')
                db.session.rollback()
        return super(SettingsPasswordView, self).post(form=form, **extra)


class SettingsEmailChangeView(BaseController):
    header = _(u'Изменение e-mail адреса')
    sidebar_path = "/helpers/account_sidebar.html"
    _messages = {
        'success': _(u'E-mail успешно изменен'),
        'internal_error': _(u'Внутренняя ошибка'),
    }
    decorators = [login_required]

    def get_current_mail(self):
        return current_user.email[:1] + '*****' + current_user.email[current_user.email.index('@'):]

    def get(self, **extra):
        return super(SettingsEmailChangeView, self).get(form=SettingsEmailChangeForm(), current_mail=self.get_current_mail(), **extra)

    def post(self, **extra):
        form = SettingsEmailChangeForm(request.form)
        if form.validate_on_submit():
            form.populate_obj(current_user)
            try:

                current_user.update(email=form.new_mail.data)
                flash(self._messages['success'], 'success')
                return redirect(url_for("account.settings"))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'danger')
                db.session.rollback()
        return super(SettingsEmailChangeView, self).post(form=form, current_mail=self.get_current_mail(), **extra)


class SignoutView(BaseController):

    def get(self):
        logout_user()
        flash(u'Успешно вышли', 'success')
        return redirect(url_for('index.page'))


account.add_url_rule('/<int:uid>/<string:secret>/reset/', view_func=AuthResetView.as_view('reset'))
account.add_url_rule('/forgot/', view_func=ForgotView.as_view('forgot'))
account.add_url_rule('/settings/', view_func=SettingsView.as_view('settings'))
account.add_url_rule('/settings/emailchange/', view_func=SettingsEmailChangeView.as_view('settings.emailchange'))
account.add_url_rule('/settings/notification/', view_func=SettingsNotificationView.as_view('settings.notification'))
account.add_url_rule('/settings/password/', view_func=SettingsPasswordView.as_view('settings.password'))
account.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
account.add_url_rule('/signout/',  view_func=SignoutView.as_view('signout'))
# account.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
