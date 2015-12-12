# -*- coding: utf-8 -*-
from flask import Blueprint

module = partners = Blueprint('partners', __name__, url_prefix='/partners')

from . import views
