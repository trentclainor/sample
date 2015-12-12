from fabric.api import run, sudo, cd, settings, task, hide, env
import platform
import os

env.hosts = ['deployment_host']

deploy_dir = "/local/www/sample"
code_dir = "~/projects/sample/"
project_dir = ""
env_dir = "/.env"
user = "www-data"
group = "www-data"


@task(default=True)
def deploy():
    with settings(hide('warnings', 'running'), warn_only=True):
        if run("test -d %s" % code_dir).failed or run("test -d %s" % deploy_dir).failed:
            full_deploy()
        with cd(code_dir):
            run("git checkout master")
            run("git pull")
    sync()
    env()
    config()
    perm()
    # uwsgi_restart()
    uwsgi_reload()
    nginx_reload()
    notify('deploy complete')


def full_deploy():
    with settings(hide('warnings', 'running'), warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("mkdir -p %s" % code_dir)
            run("git clone git@github.com:trentclainor/sample.git %s" % code_dir)
            run("git checkout -b sample1" % code_dir)
        sudo("mkdir -p -m a+rwX %s" % deploy_dir)
        sudo("chmod -R a+rwX %s" % deploy_dir)
    deploy()


def config():
    with settings(hide('warnings', 'running', 'stdout'), warn_only=True):
        with cd(deploy_dir):
            if run("test -f /etc/init/uwsgi.conf").failed:
                sudo("cp uwsgi.conf /etc/init/")
                sudo("sudo initctl reload-configuration")
                sudo("sudo service uwsgi start")
            sudo("ln -sf %s/sample.ini /etc/uwsgi/apps-enabled/sample.ini" % deploy_dir)
            sudo("ln -sf %s/nginx.conf /etc/nginx/sites-enabled/smaple.conf" % deploy_dir)
            sudo("mv settings.py.production settings.py")


def perm():
    with settings(hide('warnings', 'running', 'stdout'), warn_only=True):
        with cd(deploy_dir):
            sudo("chown -R %s:%s ." % (user, group))
            sudo("chmod -R a+rwX %s" % deploy_dir)


def env():
    with settings(hide('warnings', 'running', 'stdout'), warn_only=True):
        if run("test -d %s" % deploy_dir + env_dir).failed or run("test -d %s" % deploy_dir + env_dir + '/bin').failed:
            sudo("mkdir -p -m a+rwX %s" % deploy_dir + env_dir)
            sudo("chmod -R a+rwX %s" % deploy_dir + env_dir)
            with cd(deploy_dir + env_dir):
                sudo("virtualenv .env")
                sudo("source .env/bin/activate")
                sudo(".env/bin/pip install -r %s/requirements.txt" % deploy_dir)
        else:
            with cd(deploy_dir + env_dir):
                sudo(".env/source bin/activate")
                sudo(".env/bin/pip install -r %s/requirements.txt" % deploy_dir)


def sync():
    with settings(hide('warnings', 'running', 'stdout'), warn_only=True):
        sudo("rsync -a --exclude='.env' --checksum --delete %s %s" % (code_dir + project_dir + "/", deploy_dir))


@task
def resetdb():
    with settings(hide('warnings', 'running'), warn_only=True):
        with cd(deploy_dir + env_dir):
            run("source bin/activate")
        with cd(deploy_dir):
            run("%s/bin/python manage.py resetdb" % (deploy_dir + env_dir))


@task
def migrate():
    with settings(hide('warnings', 'running'), warn_only=True):
        with cd(deploy_dir + env_dir):
            run("source bin/activate")
        with cd(deploy_dir):
            run("%s/bin/python manage.py db migrate" % (deploy_dir + env_dir))
            run("%s/bin/python manage.py db upgrade" % (deploy_dir + env_dir))


@task
def uwsgi_reload():
    sudo('touch /etc/uwsgi/apps-enabled/sample.ini')


@task
def uwsgi_restart():
    sudo('service uwsgi restart')


@task
def uwsgi_start():
    sudo('service uwsgi start')


@task
def uwsgi_stop():
    sudo('service uwsgi stop')


@task
def nginx_reload():
    sudo('/etc/init.d/nginx reload')


def notify(msg):
    if platform.system() == 'Darwin':
        os.system(u'osascript -e \'display notification "' + msg + '"\'')
