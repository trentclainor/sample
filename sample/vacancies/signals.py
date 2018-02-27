from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from sample.common.models import MESSAGE_STATUSES
from sample.search.tasks import vacancy_score
from .models import Vacancy, Message
from .tasks import send_message


@receiver(post_save, sender=Vacancy)
def receive_score(sender, instance, **kwargs):
    transaction.on_commit(lambda: vacancy_score.delay(instance.pk))


@receiver(post_save, sender=Message)
def new_message(sender, instance, signal, created, **kwargs):
    """
    Send message to user users
    """
    if instance.status == MESSAGE_STATUSES.new:
        transaction.on_commit(lambda: send_message.delay(instance.pk))
