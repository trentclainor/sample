# -*- coding: utf-8 -*-

from flask import Blueprint

module = account = Blueprint('account', __name__, url_prefix='/account')

from . import views
