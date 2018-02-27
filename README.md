## Installation

```bash
    $ git clone git@github.com:trentclainor/sample.git
    $ cd sample
    $ git checkout -b drf
    $ git pull origin drf
```

Install required dependencies:

```bash
    $ sudo apt-get install nginx redis-server build-essential python-dev postgresql-9.6 postgresql-server-dev-9.6 python-virtualenv python-pip
```

Add ssh-public-key in the https://github.com/settings/ssh

## Database

Create DB scheme:

```bash
    $ sudo -u postgres psql

    postgres=# create user sample with password 'sample';
    CREATE ROLE
    postgres=# create database sample;
    CREATE DATABASE
    postgres=# GRANT ALL PRIVILEGES ON DATABASE sample to sample;
    GRANT
```


## Development server

```bash
    $ virtualenv --python=python3 --prompt="(sample) " .env
    $ source .env/bin/activate
    $ pip install -r requirements/local.txt
```
Create DB in database and change in settings/common.py
```bash
    $ python manage.py migrate
    $ python manage.py migrate
    $ python manage.py runserver_plus
```

## Deployment

    $ ...