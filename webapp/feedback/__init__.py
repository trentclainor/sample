# -*- coding: utf-8 -*-
from flask import Blueprint

module = Blueprint('feedback', __name__, url_prefix='/feedback')

from views import *

module.add_url_rule('/', view_func=FeedbackView.as_view('index'))
