# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms.fields import HiddenField
from flask import request, redirect, url_for
from webapp.helpers import is_safe_url, get_redirect_target


class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        form = super(RedirectForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target(request) or ''
        return form

    def redirect(self, endpoint='/', **values):
        if is_safe_url(self.next.data, request):
            return redirect(self.next.data)
        target = get_redirect_target(request)
        return redirect(target or url_for(endpoint, **values))
