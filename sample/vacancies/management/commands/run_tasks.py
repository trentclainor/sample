from django.core.management.base import BaseCommand

from sample.vacancies.tasks import process_provider
from django.conf import settings


class Command(BaseCommand):
    help = 'Load vacancies from xml files'
    all_providers = settings.PROVIDERS
    missing_args_message = ('You must provide an provider name, '
                            'a possible values: {} or argument -a'.format(', '.join(all_providers)))
    providers = []

    def add_arguments(self, parser):
        parser.add_argument(
            nargs='?',
            action='append',
            choices=self.all_providers,
            dest='providers',
            help='List of providers, a possible values: {}'.format(', '.join(self.all_providers))
        )

        parser.add_argument(
            '--all',
            '-a',
            action='store_true',
            dest='all',
            default=False,
            help='All providers',
        )

    def handle(self, *args, **options):
        self.providers = []
        if options.get('all'):
            self.providers = self.all_providers
        elif options.get('providers'):
            self.providers = options.get('providers')
        for provider in self.providers:
            print('Run task process_provider(%s)' % provider)
            process_provider.delay(provider)
