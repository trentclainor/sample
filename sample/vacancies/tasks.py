import logging
from io import StringIO

from celery.schedules import crontab
from celery.task import periodic_task, task
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import call_command

from sample.common.models import MESSAGE_STATUSES
from sample.vacancies.models import Message

logger = logging.getLogger('celery')


@task()
def process_provider(provider):
    """ Load data from xml and save in DB """
    stdout = StringIO()
    call_command('loadvacancies', provider, stdout=stdout)
    stdout = stdout.getvalue()
    return True if not stdout else stdout


@periodic_task(
    # Execute every hours: midnight, 1am, 2am, etc
    run_every=crontab(minute=0, hour='*/1'),
    name='run_providers_process',
    ignore_result=True
)
def run_providers_process():
    """ Run data loader from scrapers data files """
    providers = [
        'kpmg',
        'pwc',
        'ukcareers',
        'test',
    ]
    for provider in providers:
        process_provider.delay(provider)
    return True


@task()
def send_message(message_id):
    """Send message to user"""

    message = Message.objects.get(id=message_id)

    try:
        send_mail(
            settings.MESSAGE_SUBJECT,
            message.text,
            settings.MESSAGE_FROM,
            [message.get_mail_to()],
            fail_silently=False,
        )
        message.status = MESSAGE_STATUSES.sent
        message.status = MESSAGE_STATUSES.sent
        message.save()
        return True
    except:
        message.status = MESSAGE_STATUSES.error
        message.save()
        return False
