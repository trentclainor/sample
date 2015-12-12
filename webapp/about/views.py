# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from webapp.controller import BaseController
from flask.ext.babel import gettext as _


class AboutView(BaseController):
    template = 'about.html'
    header = _(u'О системе')
    breadcrumbs = [(_(u'О системе'), '', {})]
