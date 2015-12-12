# -*- coding: utf-8 -*-

from flask import url_for, request
from webapp.extensions import gravatar
from datetime import datetime


def common():
    return {'gravatar': gravatar, 'copyright_year': copyright_year()}


def copyright_year(start_year=2014):
    now = datetime.now()
    if start_year < now.year:
        return "{start_year} - {current_year}".format(start_year=start_year, current_year=now.year)
    return "{start_year}".format(start_year=start_year)

