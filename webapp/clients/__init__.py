# -*- coding: utf-8 -*-
from flask import Blueprint

module = clients = Blueprint('clients', __name__, url_prefix='/clients')

from . import views
