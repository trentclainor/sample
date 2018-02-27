from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from ..managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=60, null=True)
    is_candidate = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_active(self):
        return True

    @property
    def is_superuser(self):
        return self.is_admin
