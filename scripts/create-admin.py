# -*- coding: utf-8 -*-

from webapp.extensions import db
from flask.ext.script import Command as BaseCommand, prompt, prompt_pass
from webapp.models import *


class Command(BaseCommand):
    """create admin user"""

    def run(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        email, passwd = self.ask_params()
        if email and passwd:
            user = User(name=u'Admin', email=email, password=passwd, role='admin')
            db.session.add(user)
            db.session.commit()

    def ask_params(self):
        email = prompt("Choose admin email as login")
        passwd = prompt_pass("Password")
        return email, passwd
