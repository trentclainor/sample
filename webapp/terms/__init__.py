# -*- coding: utf-8 -*-
from flask import Blueprint

module = Blueprint('terms', __name__, url_prefix='/terms')

from views import *

module.add_url_rule('/', view_func=TermsView.as_view('index'))
