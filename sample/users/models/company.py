from django.db import models
from django.utils import timezone

from .user import User


class Company(models.Model):

    def logo_directory_path(instance, filename):
        """ Save Photo to reverse user directory """
        return 'logo/%s/%s' % ("/".join(list("%03d" % instance.user.id)[-3:]), filename)

    user = models.OneToOneField(User, null=True, related_name='company', on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=logo_directory_path, blank=True, null=True)
    name = models.CharField(max_length=255, blank=False)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    descr = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
