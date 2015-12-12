# -*- coding: utf-8 -*-

from flask import Blueprint

module = Blueprint('about', __name__, url_prefix='/about')

from views import *

module.add_url_rule('/', view_func=AboutView.as_view('index'))
