from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'sample.users'

    def ready(self):
        from . import signals
