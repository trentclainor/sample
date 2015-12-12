# -*- coding: utf-8 -*-

# from __future__ import unicode_literals


from flask import request, make_response
from webapp.controller import BaseController
from flask.ext.babel import gettext as _


class IndexView(BaseController):
    template = 'index.html'
    header = _(u'Welcome')

    def get(self):
        response = make_response(self.render())
        pid = request.args.get('pid')
        if pid:
            response.set_cookie('pid', int(pid))
        return response

# sdsfs sgfdsaf sdafsdaf sadfsdf sadfsd sadsd sdsads asedsds sadsadsa asdsadsa asdsdsad sadsadsadsa asdasdsa
class BlockedView(BaseController):
    template = 'blocked.html'
    header = _(u'Blocked')
