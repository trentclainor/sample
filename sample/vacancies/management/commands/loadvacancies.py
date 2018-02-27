import hashlib
import html
import os
import shutil
from datetime import datetime

import psycopg2
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from sample.common.models import City, Country, Industry, JOB_TYPES, Location, Role, State
from sample.vacancies.models import Vacancy


class Command(BaseCommand):
    help = 'Load vacancies from xml files'
    all_providers = settings.PROVIDERS
    missing_args_message = ('You must provide an provider name, '
                            'a possible values: {} or argument -a'.format(', '.join(all_providers)))
    providers = []
    workdir = None
    silent = False
    keep = True

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

        parser.add_argument(
            '--keep',
            '-k',
            action='store_true',
            dest='keep',
            default=False,
            help='Keep file after importing',
        )

        parser.add_argument(
            '--silent',
            '-s',
            action='store_true',
            dest='silent',
            default=False,
            help='Not show message when file not exist',
        )

        parser.add_argument(
            '--workdir',
            '-w',
            default=settings.SCRAPERS_DATA_DIR,
            dest='workdir',
            help='Working directory for looking import data files'
        )

        parser.add_argument(
            '--filename',
            default=None,
            dest='filename',
            help='Import file data files'
        )

    def handle(self, *args, **options):
        if options.get('providers'):
            if None not in options.get('providers'):
                self.providers = options.get('providers')
        if options.get('all'):
            self.providers = self.all_providers
        self.silent = options.get('silent')
        self.keep = options.get('keep')
        self.workdir = options.get('workdir')
        if options.get('filename'):
            self.load_xml(options.get('filename'), process=False)
            return
        for provider in self.providers:
            self.load_xml('{}.xml'.format(provider))

    def load_xml(self, filename, process=True):
        cnt = 0
        total = 0
        if process:
            filename = self._process_file(filename)
        if filename is False:
            return
        with open(filename) as fp:
            soup = BeautifulSoup(fp, "html.parser")
        for job in soup.findAll('job'):
            try:
                try:
                    job_types = []
                    if job.type:
                        job_types = self._get_job_types(job.type.text.split(','))
                    country_name = None
                    if job.country and job.country.text.strip():
                        country_name = job.country.text.strip()
                    state_name = None
                    if job.state and job.state.text.strip():
                        state_name = job.state.text.strip()
                    city_name = None
                    if job.city and job.city.text.strip():
                        city_name = job.city.text.strip()
                    # location_name = None
                    if not city_name:
                        if job.location and job.location.text.strip():
                            location = job.location.text.strip().split(',')
                            if len(location):
                                city_name = location[0]
                            if not state_name and len(location) == 3:
                                state_name = location[1]
                    country = city = state = None
                    if country_name:
                        country, created = Country.objects.get_or_create(name=html.unescape(country_name))
                    if state_name:
                        state, created = State.objects.get_or_create(name=html.unescape(state_name))
                    if city_name:
                        city, created = City.objects.get_or_create(name=html.unescape(city_name))
                    location, created = Location.objects.get_or_create(country=country, state=state, city=city)
                    industry = None
                    if job.category and job.category.text.strip():
                        industry, created = Industry.objects.get_or_create(name=html.unescape(job.category.text.strip()))
                    assert job.job_title, ('job_title not found and row skipped in:')
                    name = role_name = html.unescape(job.job_title.text.strip())
                    role, created = Role.objects.get_or_create(name=role_name)
                    source = str(job)
                    try:
                        r, created = Vacancy.objects.get_or_create(
                            location=location,
                            industry=industry,
                            role=role,
                            types=job_types,
                            name=name,
                            descr=html.unescape(job.description.text.strip()) if job.description else None,
                            source=source,
                            source_hash=hashlib.sha256(source.encode('utf-8')).hexdigest(),
                        )
                        if created:
                            cnt += 1
                    except IntegrityError:
                        continue
                except AssertionError as e:
                    self.stderr.write(self.style.ERROR("{}\n{}".format(e, job)))
            finally:
                total += 1
        if self.keep is False:
            os.remove(filename)
        if not self.silent:
            self.stdout.write(self.style.SUCCESS('{} from {}'.format(cnt, total)))

    def _get_job_types(self, jts):
        job_types = set()
        for j in jts:
            for jt in JOB_TYPES:
                if jt[1] == j.strip():
                    job_types.add(jt[0])
        return list(job_types)

    def _process_file(self, name):
        filename_tmp = '{}/{}-{}'.format(self.workdir, f"{datetime.now():%Y%m%d%H%M%S}", name)
        filename = '{}/{}'.format(self.workdir, name)
        if os.path.exists(filename) is False:
            if not self.silent:
                self.stderr.write(self.style.ERROR('{} not exist'.format(filename)))
            return False
        shutil.move(filename, filename_tmp)
        return filename_tmp
