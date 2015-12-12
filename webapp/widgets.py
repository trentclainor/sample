# -*- coding: utf-8 -*-

from wtforms.widgets import PasswordInput


class MyPasswordInput(PasswordInput):
    input_type = 'password'

    def __init__(self, hide_value=False):
        self.hide_value = hide_value

    def __call__(self, field, **kwargs):
        if self.hide_value:
            kwargs['value'] = ''
        return super(MyPasswordInput, self).__call__(field, **kwargs)
