from django.apps import AppConfig


class JobProfilesConfig(AppConfig):
    name = 'sample.job_profiles'

    def ready(self):
        from . import signals
