# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from flask import flash, request, url_for, current_app
from flask.ext.login import current_user
from .forms import FeedbackAnonymousForm, FeedbackUserForm
from webapp.controller import BaseController
from flask.ext.babel import gettext as _
from webapp.extensions import db, mail
from webapp.models import Feedback
from flask.ext.mail import Message


class FeedbackView(BaseController):
    header = _(u'Обратная связь')
    breadcrumbs = [(u'Обратная связь', '', {})]
    _messages = {
        'success': _(u'Обращение успешно отправленно'),
        'internal_error': _(u'Внутренняя ошибка'),
    }

    def get(self, **extra):
        if current_user.is_authenticated():
            form = FeedbackUserForm()
        else:
            form = FeedbackAnonymousForm()
            form.email.data = request.args.get('email')
            form.text.rows = 10
        return super(FeedbackView, self).get(form=form, **extra)

    def post(self, **extra):
        if current_user.is_authenticated():
            form = FeedbackUserForm(request.form)
        else:
            form = FeedbackAnonymousForm(request.form)
        if form.validate_on_submit():
            try:
                if current_user.is_authenticated():
                    feedback = Feedback(text=form.text.data, user_id=current_user.get_id(), mail=current_user.email, name=current_user.name)
                else:
                    feedback = Feedback(text=form.text.data, mail=form.email.data, name=form.name.data)
                db.session.add(feedback)
                db.session.commit()
                flash(self._messages['success'], 'success')
                return self.redirect(url_for("feedback.index"))
            except Exception, e:
                if current_app.config['DEBUG']:
                    raise e
                else:
                    flash(self._messages['internal_error'], 'error')
                db.session.rollback()
        return super(FeedbackView, self).post(form=form, **extra)
