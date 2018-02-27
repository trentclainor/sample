from django.apps import AppConfig


class VacanciesConfig(AppConfig):
    name = 'sample.vacancies'

    def ready(self):
        from . import signals
