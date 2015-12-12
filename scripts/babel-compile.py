# -*- coding: utf-8 -*-

from os.path import isdir
import subprocess
from flask.ext.script import Command as BaseCommand


class Command(BaseCommand):
    """Compile babel translations"""

    def run(self, *args, **kwargs):
        command = "pybabel compile -f -d {dir}".format(dir='webapp/translations')
        print "Command:", command
        subprocess.call(command.split())
