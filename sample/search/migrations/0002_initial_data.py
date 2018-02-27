# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-01 11:13
from __future__ import unicode_literals

import os

import psycopg2
from django.conf import settings
from django.db import connections, migrations
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def initial_data(apps, schema_editor):
    file_path = os.path.join(os.path.dirname(__file__), '../sql/', 'initial-data.sql')
    sql_statement = open(file_path).read()
    with connections['matching'].cursor() as cursor:
        cursor.execute(sql_statement)


def predefined_data(apps, schema_editor):
    file_path = os.path.join(os.path.dirname(__file__), '../sql/', 'predefined-data.sql')
    sql_statement = open(file_path).read()
    with connections['matching'].cursor() as cursor:
        cursor.execute(sql_statement)


def create_db(apps, schema_editor):
    db1 = settings.DATABASES.get('default')
    db2 = settings.DATABASES.get('matching')
    conn_params = {'database': db1['NAME']}
    if db1.get('USER'):
        conn_params['user'] = db1.get('USER')
    if db1.get('PASSWORD'):
        conn_params['password'] = db1.get('PASSWORD')
    if db1.get('HOST'):
        conn_params['host'] = db1.get('HOST')
    if db1.get('PORT'):
        conn_params['port'] = db1.get('PORT')
    conn = psycopg2.connect(**conn_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("select exists(select * from pg_catalog.pg_database where datname='{}')".format(db2['NAME']))
    if cur.fetchone()[0] != True:
        cur.execute("CREATE DATABASE {}".format(db2['NAME']))
        initial_data(apps, schema_editor)
        predefined_data(apps, schema_editor)
    conn.close()


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_db),
    ]
