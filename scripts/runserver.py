# -*- coding: utf-8 -*-

import subprocess
from webapp.extensions import db
from flask.ext.script import Command as BaseCommand


class Command(BaseCommand):
    """clean all .pyc files"""

    def run(self):
        clean_command = "find . -name *.pyc -delete".split()
        subprocess.call(clean_command)

