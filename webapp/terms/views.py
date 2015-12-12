# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from webapp.controller import BaseController
from flask.ext.babel import gettext as _


class TermsView(BaseController):
    template = 'terms.html'
    header = _(u'Условия использования')
    breadcrumbs = [(_(u'Условия использования'), '', '')]
