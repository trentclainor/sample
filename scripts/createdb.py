# -*- coding: utf-8 -*-

from webapp.extensions import db
from flask.ext.script import Command as BaseCommand, prompt_bool
from webapp.models import *


class Command(BaseCommand):
    """create scheme"""

    def run(self):
        import logging
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.orm').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        if prompt_bool("Create all table in db?"):
            db.create_all()
