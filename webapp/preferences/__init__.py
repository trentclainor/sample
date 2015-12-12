# -*- coding: utf-8 -*-
from flask import Blueprint

module = preferences = Blueprint('preferences', __name__, url_prefix='/preferences')

from . import views
