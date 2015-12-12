#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import coloredlogs
from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from webapp import app
from webapp.extensions import db
from scripts import scripts
from webapp.extensions import evolution
# from migrate.versioning.shell import main

coloredlogs.DEFAULT_DATE_FORMAT = '%H:%M:%S'
coloredlogs.install(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-15s - %(levelname)s: %(message)s"
)

migrate = Migrate(app, db)
manager = Manager(app)

scripts('scripts', manager)

manager.add_command('db', MigrateCommand)


@manager.command
def migrate(action):
    evolution(app).manager(action)


manager.add_command('shell', Shell(make_context=lambda: {'app': app, 'db': db}))
manager.add_command("runserver", Server(
    use_reloader=True,
    host='0.0.0.0',
    port=5000,
))

if __name__ == '__main__':
    manager.run()
