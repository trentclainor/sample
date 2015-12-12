# -*- coding: utf-8 -*-
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.gravatar import Gravatar
# from flask.ext.email import ConsoleMail
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from flask.ext.evolution import Evolution
from flask.ext.principal import Principal
from flask.ext.wtf.csrf import CsrfProtect

db = SQLAlchemy()
login_manager = LoginManager()

def mail(app):
    return Mail(app)


def gravatar(app):
    return Gravatar(app, size=200, rating='g', default='blank')


def toolbar(app):
    return DebugToolbarExtension(app)


def babel(app):
    return Babel(app)


def evolution(app):
    return Evolution(app)


def principal(app):
    return Principal(app)


def csrf(app):
    return CsrfProtect(app)
