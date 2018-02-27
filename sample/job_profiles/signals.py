import hashlib
import time

from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from sample.job_profiles.utils import document_to_html
from sample.search.tasks import job_profile_score
from .models import JobProfile


@receiver(pre_save, sender=JobProfile)
def update_job_profile(sender, instance, **kwargs):
    """
    if set is_default=True, set is_default=False to another user job profiles
    """
    if instance.is_default:
        JobProfile.objects.filter(user=instance.user).update(is_default=False)


@receiver(post_save, sender=JobProfile)
def convert_cv(sender, instance, **kwargs):
    """
    Convert cv from (many formats: rtf, doc, pdf, odt..) to html/txt format
    """
    if instance.cv:
        content = document_to_html(instance.cv.file, format='html')
        cv_content_hash = hashlib.sha256(content).hexdigest()
        sender.objects.update(cv_content=content, cv_content_hash=cv_content_hash)


@receiver(post_save, sender=JobProfile)
def receive_score(sender, instance, **kwargs):
    transaction.on_commit(lambda: job_profile_score.delay(instance.pk))
