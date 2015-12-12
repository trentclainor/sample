# -*- coding: utf-8 -*-

from flask import Blueprint

module = Blueprint('index', __name__, url_prefix='/')


from views import *

module.add_url_rule('', view_func=IndexView.as_view('page'))
module.add_url_rule('blocked/', view_func=BlockedView.as_view('blocked'))
