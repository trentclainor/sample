from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

User = get_user_model()

JOB_TYPES = Choices(
    (0, 'full_time', _('Full Time')),
    (1, 'part_time', _('Part Time')),
    (2, 'contract', _('Contract')),
    (3, 'permanent', _('Permanent')),
    (4, 'temporary', _('Temporary')),
)

LANG_LEVELS = Choices(
    (0, 'basic', _('Basic')),
    (1, 'business', _('Business')),
    (2, 'fluent', _('Fluent')),
)

MESSAGE_STATUSES = Choices(
    (0, 'new', _('New')),
    (1, 'sent', _('Sent')),
    (2, 'error', _('Sent with error')),
)


class Industry(models.Model):
    name = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=255, unique=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Location(models.Model):
    country = models.ForeignKey(Country, blank=True, null=True, related_name='country', on_delete=models.CASCADE)
    state = models.ForeignKey(State, blank=True, null=True, related_name='state', on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=True, null=True, related_name='city', on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('country', 'state', 'city')

    def __str__(self):
        if self.city and self.state and self.country:
            return ("{0}, {1}, {2}").format(self.city, self.state, self.country)
        elif self.state and self.country:
            return ("{0}, {1}").format(self.state, self.country)
        elif self.city and self.country:
            return ("{0}, {1}").format(self.city, self.country)
        elif self.country:
            return ("{0}").format(self.country)
        return ("{0}, {1}, {2}").format(self.city if self.city else '-', self.state if self.state else '-',
                                        self.country if self.country else '-')

    name = property(__str__)


class ExternalRole(models.Model):
    title_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    title_tally = models.IntegerField(null=False, default=1)

    class Meta:
        db_table = 'titles_clean'


class ExternalSkill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'skills'
