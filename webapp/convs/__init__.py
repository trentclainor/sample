# -*- coding: utf-8 -*-

from flask import Blueprint

module = convs = Blueprint('convs', __name__, url_prefix='/convs')

from . import views
