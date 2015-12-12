# -*- coding: utf-8 -*-
from webapp.extensions import db
from flask.ext.script import Command as BaseCommand, prompt_bool
from webapp.models import *
from random import randint


class Command(BaseCommand):
    """create scheme"""

    def run(self):
        import logging
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.orm').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        if prompt_bool("Recreate all table in db?"):
            db.drop_all()
            db.create_all()
