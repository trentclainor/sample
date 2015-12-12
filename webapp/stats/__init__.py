# -*- coding: utf-8 -*-

from flask import Blueprint

module = stats = Blueprint('stats', __name__, url_prefix='/stats')

from . import views
