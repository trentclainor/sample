import urllib.parse

from django.db.models import Avg, Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.search.serializers import SearchJobProfileSerializer
from sample.job_profiles.models import JobProfile
from sample.tests.factories import (CityFactory, CompanyFactory, CountryFactory, IndustryFactory, JobProfileFactory,
                                       JobProfileVacancyFactory, LocationFactory, PreferencesFactory, RecruiterFactory,
                                       RoleFactory, StateFactory, VacancyFactory)


class SearchJobProfileTestCase(APITestCase):
    client_class = APIClient
    user = None
    company = None
    list_url = reverse('search-job-profiles-list')
    vacancies = []
    job_profiles = []
    industries = []
    locations = []
    maxDiff = None

    def url_with_querystring(self, path, *args, **kwargs):
        if args:
            return '{}?{}'.format(path, urllib.parse.urlencode(args, doseq=True))
        return '{}?{}'.format(path, urllib.parse.urlencode(kwargs))

    def create_job_profiles(self, vacancy_idx=None):
        self.vacancies = [
            VacancyFactory(name='Vacancy 1', company=self.user.company),
            VacancyFactory(name='Vacancy 2', company=self.user.company),
        ]
        countries = [
            CountryFactory(name='UK'),
            CountryFactory(name='USA'),
        ]
        states = [
            StateFactory(name='Kent'),
            StateFactory(name='Arizona'),
            StateFactory(name='Colorado'),
        ]
        cities = [
            CityFactory(name='Maidstone'),
            CityFactory(name='London'),
            CityFactory(name='Phoenix'),
            CityFactory(name='Denver'),
        ]
        self.locations = l = [
            LocationFactory(country=countries[0], state=states[0], city=cities[0]),  # 0, Maidstone, Kent, UK
            LocationFactory(country=countries[0], state=None, city=cities[1]),  # 1, London, UK
            LocationFactory(country=countries[0], state=None, city=None),  # 2, UK
            LocationFactory(country=countries[1], state=states[1], city=cities[2]),  # 3, Phoenix, Arizona, USA
            LocationFactory(country=countries[1], state=None, city=cities[3]),  # 4, Denver, USA
            LocationFactory(country=countries[1], state=None, city=None),  # 5, USA
        ]
        self.industries = i = [
            IndustryFactory(name='Finance'),  # 0
            IndustryFactory(name='Freelance'),  # 1
            IndustryFactory(name='Medicine'),  # 2
            IndustryFactory(name='Education'),  # 3
            IndustryFactory(name='Entertainment'),  # 4
        ]
        self.roles = r = [
            RoleFactory(name='Account Manager 0'),
            RoleFactory(name='Freelancer 1'),
            RoleFactory(name='Doctor 2'),
        ]
        self.job_profiles = j = [
            JobProfileFactory(name='Job profile 0', is_default=True),
            JobProfileFactory(name='Job profile 1 Actor', is_default=True),
            JobProfileFactory(name='Job profile 2', is_default=True),
            JobProfileFactory(name='Job profile 3 Doctor', is_default=True),
            JobProfileFactory(name='Job profile 4', is_default=True),
            JobProfileFactory(name='Job profile 5', is_default=True),
        ]
        # self.location = LocationFactory()
        self.roles = RoleFactory.create_batch(3)
        self.preferences = [
            PreferencesFactory(
                job_profile=j[0],
                industries=(i[0], i[2]),
                looking_for=[0, 1, 3],
                roles=(r[0], r[2]),
                location=l[1],
            ),
            PreferencesFactory(
                job_profile=j[1],
                industries=(i[0], i[3]),
                looking_for=[1, 2],
                roles=(r[0], r[2]),
                location=l[1],
            ),
            PreferencesFactory(
                job_profile=j[2],
                industries=(i[0], i[1], i[2]),
                looking_for=[0, 1, 2, 3],
                roles=(r[0], r[2]),
                location=None,
            ),
            PreferencesFactory(
                job_profile=j[3],
                industries=(i[3], i[4]),
                looking_for=[0, 3],
                roles=(r[0], r[2]),
                location=l[4],
            ),
            PreferencesFactory(
                job_profile=j[4],
                industries=(i[0], i[1]),
                looking_for=[1, 2],
                roles=(r[0], r[2]),
                location=l[3],
            ),
            PreferencesFactory(
                job_profile=j[5],
                industries=(i[0], i[2]),
                looking_for=[0, 2],
                roles=(r[0], r[2]),
                location=l[1],
            ),
        ]
        JobProfileVacancyFactory(job_profile=self.job_profiles[0], vacancy=self.vacancies[0], score=0.9)
        JobProfileVacancyFactory(job_profile=self.job_profiles[1], vacancy=self.vacancies[0], score=1.1)
        JobProfileVacancyFactory(job_profile=self.job_profiles[2], vacancy=self.vacancies[0], score=1.2)
        JobProfileVacancyFactory(job_profile=self.job_profiles[3], vacancy=self.vacancies[0], score=0.9)
        JobProfileVacancyFactory(job_profile=self.job_profiles[4], vacancy=self.vacancies[0], score=1.1)
        JobProfileVacancyFactory(job_profile=self.job_profiles[5], vacancy=self.vacancies[0], score=1.2)
        JobProfileVacancyFactory(job_profile=self.job_profiles[1], vacancy=self.vacancies[1], score=1.3)
        JobProfileVacancyFactory(job_profile=self.job_profiles[2], vacancy=self.vacancies[1], score=1.5)
        JobProfileVacancyFactory(job_profile=self.job_profiles[3], vacancy=self.vacancies[1], score=1.6)
        queryset = JobProfile.objects.filter(is_published=True, is_default=True, user__is_candidate=True)
        if vacancy_idx is not None:
            vacancies = [self.vacancies[vacancy_idx]]
        else:
            vacancies = self.vacancies
        queryset = queryset.filter(jobprofilevacancy__vacancy__in=vacancies)
        queryset = queryset.annotate(score=Avg('jobprofilevacancy__score'))
        queryset = queryset.exclude(user=self.user)
        return queryset

    def setUp(self):
        self.user = RecruiterFactory(company=self.company)
        self.company = CompanyFactory(user=self.user)
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_return_401(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_return_all_matches_job_profiles(self):
        job_profiles = self.create_job_profiles()
        job_profiles = job_profiles.order_by('id')
        response = self.client.get(self.url_with_querystring(
            self.list_url,
            ('ordering', 'id'),
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchJobProfileSerializer(job_profiles, many=True).data)

    def test_get_list_by_vacancy_should_return_all_matches_job_profiles(self):
        job_profiles = self.create_job_profiles(vacancy_idx=0)
        vacancy = self.vacancies[0]
        response = self.client.get(self.url_with_querystring(self.list_url, **{
            'vacancy_id': vacancy.id,
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchJobProfileSerializer(job_profiles, many=True).data)

    def test_filter_with_types_query_should_apply_name_filter_on_results(self):
        job_profiles = self.create_job_profiles(vacancy_idx=0)
        job_profiles = job_profiles.filter(preferences__looking_for__overlap=[0])
        job_profiles = job_profiles.order_by('id')
        vacancy = self.vacancies[0]
        response = self.client.get(self.url_with_querystring(
            self.list_url,
            ('vacancy_id', vacancy.id),
            ('types', 0),
            ('types', 4),
            ('ordering', 'id'),
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchJobProfileSerializer(job_profiles, many=True).data)
        self.assertEqual([job_profile for job_profile in job_profiles], [
            self.job_profiles[0],
            self.job_profiles[2],
            self.job_profiles[3],
            self.job_profiles[5],
        ])

    def test_filter_name_should_apply_name_filter_on_results(self):
        """Filter name"""
        job_profiles = self.create_job_profiles(vacancy_idx=0)
        job_profiles = job_profiles.filter(name__icontains='tor')
        job_profiles = job_profiles.order_by('name')
        vacancy = self.vacancies[0]
        response = self.client.get(self.url_with_querystring(self.list_url, **{
            'vacancy_id': vacancy.id,
            'name': 'tor',
            'ordering': 'name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchJobProfileSerializer(job_profiles, many=True).data)
        self.assertEqual([job_profile for job_profile in job_profiles], [
            self.job_profiles[1],
            self.job_profiles[3],
        ])

    def test_filter_industry_should_apply_industry_filter_on_results(self):
        """ Filter Medicine and Education """
        search = 'ed'
        job_profiles = self.create_job_profiles(vacancy_idx=0)
        job_profiles = job_profiles.filter(preferences__industries__name__icontains=search)
        job_profiles = job_profiles.order_by('-name')
        vacancy = self.vacancies[0]
        response = self.client.get(self.url_with_querystring(self.list_url, **{
            'vacancy_id': vacancy.id,
            'industry': search,
            'ordering': '-name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchJobProfileSerializer(job_profiles, many=True).data)
        self.assertEqual([job_profile for job_profile in job_profiles], [
            self.job_profiles[5],
            self.job_profiles[3],
            self.job_profiles[2],
            self.job_profiles[1],
            self.job_profiles[0],
        ])

    def test_search_location_should_search_rows_with_locations(self):
        """ Search Kent, Phoenix, Denver """
        search = 'en'
        job_profiles = self.create_job_profiles(vacancy_idx=0)
        job_profiles = job_profiles.filter(Q(preferences__location__city__name__icontains=search) | Q(
            preferences__location__state__name__icontains=search) | Q(
            preferences__location__country__name__icontains=search))
        job_profiles = job_profiles.order_by('name')
        vacancy = self.vacancies[0]
        response = self.client.get(self.url_with_querystring(self.list_url, **{
            'vacancy_id': vacancy.id,
            'search': search,
            'ordering': 'name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchJobProfileSerializer(job_profiles, many=True).data)
        self.assertEqual([job_profile for job_profile in job_profiles], [
            self.job_profiles[3],
            self.job_profiles[4],
        ])

    def test_ordering_should_apply_ordering_to_rows(self):
        job_profiles = self.create_job_profiles(vacancy_idx=1)
        job_profiles = job_profiles.order_by('-name')
        vacancy = self.vacancies[1]
        response = self.client.get(self.url_with_querystring(self.list_url, **{
            'vacancy_id': vacancy.id,
            'ordering': '-name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchJobProfileSerializer(job_profiles, many=True).data)
        self.assertEqual([job_profile for job_profile in job_profiles], [
            self.job_profiles[3],
            self.job_profiles[2],
            self.job_profiles[1],
        ])
