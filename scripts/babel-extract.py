# -*- coding: utf-8 -*-

from os.path import isdir
import subprocess
from flask.ext.script import Command as BaseCommand, Option


class Command(BaseCommand):
    """Extract babel translations"""

    def run(self, *args, **kwargs):
        command = "pybabel extract -F babel.cfg -o {message_file} .".format(message_file='messages.pot')
        print "Command:", command
        subprocess.call(command.split())
