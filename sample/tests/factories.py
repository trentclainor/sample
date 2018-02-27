import datetime

import factory
from django.contrib.auth import get_user_model
from factory.fuzzy import FuzzyDate

from sample.common.models import City, Country, Industry, Location, Role, State
from sample.job_profiles.models import (BasicInfo, Education, JOB_TYPES, JobProfile, LANG_LEVELS, Language,
                                           Preferences, WorkHistory)
from sample.search.models import JobProfileVacancy
from sample.vacancies.models import Company, Vacancy

User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    name = factory.Sequence(lambda i: 'Tom {0}'.format(i))
    email = factory.Sequence(lambda i: 'user{0}@example.com'.format(i))
    is_candidate = False
    is_recruiter = False

    password = '123456'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # if cls.is_candidate:
        #     Company.objects.update_or_create(user=cls, defaults=cls.company)
        #
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('company')


class CandidateFactory(UserFactory):
    is_candidate = True


class RecruiterFactory(UserFactory):
    is_recruiter = True


class JobProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = JobProfile

    user = factory.SubFactory(CandidateFactory)
    name = factory.Sequence(lambda n: 'job {0}'.format(n))
    is_published = True
    is_default = False


class BasicInfoFactory(factory.DjangoModelFactory):
    class Meta:
        model = BasicInfo

    name = factory.Faker('name')
    email = factory.Sequence(lambda e: 'email{0}@example.com'.format(e))
    phone = factory.Sequence(lambda n: '555-55-5{0}'.format(n))
    job_profile = factory.SubFactory(JobProfileFactory)


class WorkHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = WorkHistory

    role = factory.Faker('job')
    company_name = factory.Faker('company')
    job_type = JOB_TYPES.part_time
    start_date = factory.fuzzy.FuzzyDate(start_date=datetime.date(2000, 1, 1))
    end_date = datetime.date(2002, 1, 1)
    job_profile = factory.SubFactory(JobProfileFactory)


class EducationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Education

    school = 'Oxford'
    degree = 'PhD'
    start_date = factory.fuzzy.FuzzyDate(start_date=datetime.date(2000, 1, 1))
    end_date = datetime.date(2007, 1, 1)
    job_profile = factory.SubFactory(JobProfileFactory)


class LanguageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Language

    name = 'English'
    level = LANG_LEVELS.business
    job_profile = factory.SubFactory(JobProfileFactory)


class IndustryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Industry

    name = factory.Sequence(lambda n: "Industry #%s" % n)


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Sequence(lambda n: "Role #%s" % n)


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Sequence(lambda n: 'Country {0}'.format(n))


class StateFactory(factory.DjangoModelFactory):
    class Meta:
        model = State

    name = factory.Sequence(lambda n: 'State {0}'.format(n))


class CityFactory(factory.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Sequence(lambda n: 'City {0}'.format(n))


class LocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Location

    country = factory.SubFactory(CountryFactory)
    state = factory.SubFactory(StateFactory)
    city = factory.SubFactory(CityFactory)


class PreferencesFactory(factory.DjangoModelFactory):
    class Meta:
        model = Preferences

    job_profile = factory.SubFactory(JobProfileFactory)
    location = factory.SubFactory(LocationFactory)

    @factory.post_generation
    def industries(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for industry in extracted:
                self.industries.add(industry)

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for role in extracted:
                self.roles.add(role)


class VacancyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Vacancy

    name = factory.Sequence(lambda d: "Vacancy #%s" % d)
    descr = factory.Faker('text')
    company = factory.SubFactory(CompanyFactory)
    industry = factory.SubFactory(IndustryFactory)
    role = factory.SubFactory(RoleFactory)


class JobProfileVacancyFactory(factory.DjangoModelFactory):
    class Meta:
        model = JobProfileVacancy

    score = 0.9
