import hashlib
from datetime import datetime

from array_field_select.fields import ArrayField
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from sample.common.models import Industry, JOB_TYPES, LANG_LEVELS, Location, Role
from sample.job_profiles.utils import document_to_html

User = get_user_model()


class JobProfile(models.Model):
    def cv_directory_path(instance, filename):
        """ Save CV to reverse user directory """
        return 'cv/%s/%s' % ("/".join(list("%03d" % instance.user.id)[-3:]), filename)

    user = models.ForeignKey(User, related_name='job_profiles', on_delete=models.CASCADE)
    # cv = models.FileField(upload_to='cv/%Y/%m/%d/', blank=True, null=True)
    cv = models.FileField(upload_to=cv_directory_path, blank=True, null=True)
    cv_hash = models.CharField(max_length=255, blank=True, null=True, default=None)
    cv_content = models.TextField(blank=True, null=True)
    cv_content_hash = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    is_published = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def experience(self):
        delta = relativedelta()
        for work_history in self.work_histories.all():
            delta += work_history.experience
        return delta

    class Meta:
        ordering = ('-modified', 'name')

    def __str__(self):
        if self.is_default:
            return ("{0} ({1}) - default").format(self.name, self.user.email)
        return ("{0} ({1})").format(self.name, self.user.email)

    def get_content(self):
        content = self.cv_content
        if not self.cv_content:
            for work_history in self.work_histories.all():
                content += '{}\n{}\n{}\n{}'.format(work_history.company_name, work_history.role, work_history.descr)
        return content

    def save(self, *args, **kwargs):
        if self.cv:
            self.cv_hash = hashlib.sha256(self.cv.read()).hexdigest()
        super(JobProfile, self).save(*args, **kwargs)


class BasicInfo(models.Model):
    def photo_directory_path(instance, filename):
        """ Save Photo to reverse user directory """
        return 'photo/%s/%s' % ("/".join(list("%03d" % instance.job_profile.user.id)[-3:]), filename)

    job_profile = models.OneToOneField(JobProfile, related_name='basic_info', on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, null=True)
    photo = models.ImageField(upload_to=photo_directory_path, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.email:
            return ("{0} ({1})").format(self.name, self.email)
        return self.name


class WorkHistory(models.Model):
    job_profile = models.ForeignKey(JobProfile, related_name='work_histories', on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    descr = models.TextField(blank=True)
    job_type = models.IntegerField(choices=JOB_TYPES, default=JOB_TYPES.full_time)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('start_date', 'end_date')

    def get_job_type_display(self):
        return JOB_TYPES[self.job_type]

    @property
    def experience(self):
        if self.end_date is None:
            self.end_date = datetime.utcnow()
        return relativedelta(self.end_date, self.start_date)

    def __str__(self):
        return ("{0} {1}").format(self.company_name, self.role)


class Education(models.Model):
    job_profile = models.ForeignKey(JobProfile, related_name='educations', on_delete=models.CASCADE)
    school = models.CharField(max_length=255)
    # todo: degree maybe make a choices field
    # todo: need variants for dictionary or make additional dictionary model
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('start_date', 'end_date')

    def __str__(self):
        start_date = f"{self.start_date:%B %Y}"
        if not self.end_date:
            return ("{0} {1} ({2} - present)").format(self.school, self.degree, start_date)
        return ("{0} {1} ({2} to {3})").format(self.school, self.degree, start_date, f"{self.end_date:%B %Y}")


class Language(models.Model):
    job_profile = models.ForeignKey(JobProfile, related_name='languages', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    level = models.IntegerField(choices=LANG_LEVELS, default=LANG_LEVELS.fluent)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_level_display(self):
        return LANG_LEVELS[self.level]

    def __str__(self):
        return ('{0} ({1})').format(self.name, self.get_level_display())


class Preferences(models.Model):
    job_profile = models.OneToOneField(JobProfile, related_name='preferences', on_delete=models.CASCADE)
    industries = models.ManyToManyField(Industry, related_name='industries', blank=True)
    roles = models.ManyToManyField(Role, related_name='roles', blank=True)
    location = models.ForeignKey(Location, related_name='locations', on_delete=models.CASCADE, blank=True, null=True)
    looking_for = ArrayField(models.IntegerField(
        choices=JOB_TYPES, blank=True, null=True), default=[], blank=True, null=True)
    weekly_email = models.BooleanField(default=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_looking_for_display(self):
        return [JOB_TYPES[looking_for] for looking_for in self.looking_for]
