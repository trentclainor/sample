# -*- coding: utf-8 -*-

import subprocess
from flask.ext.script import Command as BaseCommand, Option


class Command(BaseCommand):
    """Update babel translations"""

    def __init__(self, default_name='ru'):
        self.default_name = default_name

    def get_options(self):
        return [
            Option('-l', '--locale', dest='locale', default=self.default_name),
        ]

    def run(self, *args, **kwargs):
        command = "pybabel update -i messages.pot -d {dir} -l {locale}".format(dir='webapp/translations', locale=kwargs['locale'])
        print "Command:", command
        subprocess.call(command.split())
