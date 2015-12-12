# -*- coding: utf-8 -*-

from flask import Blueprint

module = clicks = Blueprint('clicks', __name__, url_prefix='/clicks')

from . import views
