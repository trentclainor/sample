## Installation

    $ git clone git@github.com:trentclainor/sample.git
    $ cd sample
    $ git checkout -b sample1
    $ git pull origin sample1

Install required dependencies:

    $ sudo apt-get install nginx redis-server build-essential python-dev postgresql-9.4 postgresql-server-dev-9.4 python-virtualenv python-pip
    $ pip install uwsgi
    $ sudo ln -fs /usr/local/bin/uwsgi /usr/bin/uwsgi
    $ sudo mkdir -p /etc/uwsgi/apps-enabled
    $ sudo mkdir /var/log/uwsgi
    
    Add ssh-public-key в https://github.com/settings/ssh
    

## Development server

    $ virtualenv --prompt="(sample) " .env
    $ source .env/bin/activate
    $ cp settings.proction.py settings.py
    $ pip install -r requirements.txt

    Create DB in database and change in settings.py
    
    $ python manage.py createdb
    $ python manage.py create-admin
    $ python manage.py runserver


## Create DB

Create DB scheme:

    $ sudo -u postgres psql

    postgres=# create user sample with password 'sample';
    CREATE ROLE
    postgres=# create database sample;
    CREATE DATABASE
    postgres=# GRANT ALL PRIVILEGES ON DATABASE sample to sample;
    GRANT

    

## Deployment

    $ fab