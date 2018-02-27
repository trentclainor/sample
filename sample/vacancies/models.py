import hashlib

from array_field_select.fields import ArrayField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from sample.common.models import Industry, JOB_TYPES, Location, MESSAGE_STATUSES, Role
from sample.job_profiles.models import JobProfile
from sample.users.models import Company

User = get_user_model()


class Vacancy(models.Model):
    location = models.ForeignKey(Location, blank=True, null=True, related_name='vacancies', on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, blank=True, null=True, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, blank=True, null=True, related_name='vacancies', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, blank=True, null=True, related_name='vacancies', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    types = ArrayField(models.IntegerField(choices=JOB_TYPES, blank=True, null=True), default=[], blank=True, null=True)
    experience_from = models.IntegerField(blank=True, null=True, default=None)
    experience_to = models.IntegerField(blank=True, null=True, default=None)
    salary_from = models.DecimalField(blank=True, null=True, default=None, decimal_places=2, max_digits=11)
    salary_to = models.DecimalField(blank=True, null=True, default=None, decimal_places=2, max_digits=11)
    descr = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    source_hash = models.CharField(max_length=255, blank=True, null=True, unique=True, default=None)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-modified', 'name')

    def __str__(self):
        return self.name

    def get_types_display(self):
        return [JOB_TYPES[t] for t in self.types]

    def get_content(self):
        content = self.source
        if not self.source:
            content = '{}\n{}\n{}\n{}'.format(self.company, self.name, self.role, self.descr)
        return content

    def save(self, *args, **kwargs):
        if self.source:
            self.source_hash = hashlib.sha256(self.source.encode('utf-8')).hexdigest()
        super(Vacancy, self).save(*args, **kwargs)


class Message(models.Model):
    vacancy = models.ForeignKey(Vacancy, related_name='vacancy', on_delete=models.CASCADE)
    job_profile = models.ForeignKey(JobProfile, related_name='job_profile', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    status = models.IntegerField(choices=MESSAGE_STATUSES, default=MESSAGE_STATUSES.new)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_mail_to(self):
        if hasattr(self.job_profile, 'basic_info') and self.job_profile.basic_info.email:
            return self.job_profile.basic_info.email
        return self.job_profile.user.email

    def __str__(self):
        return '{} -> {} ({})'.format(self.vacancy, self.get_mail_to(), self.status)
