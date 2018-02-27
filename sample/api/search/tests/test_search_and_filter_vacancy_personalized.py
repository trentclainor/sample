import urllib.parse

from django.db.models import F, Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.search.serializers import SearchVacancyPersonalizedSerializer
from sample.tests.factories import (CandidateFactory, CityFactory, CountryFactory, IndustryFactory,
                                       JobProfileFactory, JobProfileVacancyFactory, LocationFactory, PreferencesFactory,
                                       RoleFactory, StateFactory, VacancyFactory)
from sample.vacancies.models import Vacancy


class SearchVacancyPersonalizedTestCase(APITestCase):
    client_class = APIClient
    user = None
    job_profiles = []
    preferences = []
    vacancies = []
    industries = []
    locations = []
    roles = []
    list_url = reverse('search-vacancies-personalized-list')
    maxDiff = None

    def url_with_querystring(self, path, *args, **kwargs):
        if args:
            return '{}?{}'.format(path, urllib.parse.urlencode(args, doseq=True))
        return '{}?{}'.format(path, urllib.parse.urlencode(kwargs))

    def create_vacancies(self, job_profile_idx=1):
        self.job_profiles = j = [
            JobProfileFactory.create(user=self.user),
            JobProfileFactory.create(user=self.user, is_default=True),
            JobProfileFactory.create(user=self.user),
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
            IndustryFactory(name='Finance 0'),
            IndustryFactory(name='Medicine 1'),
            IndustryFactory(name='Education 2'),
        ]
        self.roles = r = [
            RoleFactory(name='Account Manager 0'),
            RoleFactory(name='Freelancer 1'),
            RoleFactory(name='Doctor 2'),
        ]
        self.vacancies = [
            VacancyFactory(location=l[0], industry=i[0], role=r[0], types=list({0, 0, 0}), name='Vacancy 0 s1'),
            VacancyFactory(location=l[1], industry=i[1], role=r[1], types=list({1, 1, 1}), name='Vacancy 1'),
            VacancyFactory(location=l[2], industry=i[1], role=r[0], types=list({0, 1, 1}), name='Vacancy 2'),
            VacancyFactory(location=l[3], industry=i[2], role=r[1], types=list({1, 2, 2}), name='Vacancy 3'),
            VacancyFactory(location=l[4], industry=i[0], role=r[0], types=list({0, 1, 1}), name='Vacancy 4 s3'),
            VacancyFactory(location=l[3], industry=i[0], role=r[1], types=list({0, 2, 2}), name='Vacancy 5'),
            VacancyFactory(location=l[2], industry=i[2], role=r[0], types=list({1, 2, 3}), name='Vacancy 6 s2'),
            VacancyFactory(location=l[4], industry=i[0], role=r[1], types=list({1, 2, 3}), name='Vacancy 7'),
        ]
        self.preferences = [
            PreferencesFactory(
                job_profile=j[0],
                industries=(i[0], i[2]),
                location=l[0],
                looking_for=[0, 1],
                roles=(r[0],),
            ),
            PreferencesFactory(
                job_profile=j[1],
                industries=(i[0],),
                location=l[4],
                looking_for=[0, 2],
                roles=(r[0], r[1]),
            ),
            PreferencesFactory(
                job_profile=j[2],
                industries=(i[0], i[1], i[2]),
                looking_for=[2, 3],
                roles=(r[0], r[1]),
                location=None,
            ),
        ]
        for vacancy in self.vacancies:
            JobProfileVacancyFactory(vacancy=vacancy, job_profile=self.job_profiles[0], score=0.9)
            JobProfileVacancyFactory(vacancy=vacancy, job_profile=self.job_profiles[1], score=1.0)
            JobProfileVacancyFactory(vacancy=vacancy, job_profile=self.job_profiles[2], score=1.1)
        queryset = Vacancy.objects.select_related('location', 'location__city', 'location__country', 'industry',
                                                  'company', 'company__user', 'role').all()
        job_profile = j[job_profile_idx]
        queryset = queryset.filter(jobprofilevacancy__job_profile=job_profile)
        queryset = queryset.annotate(score=F('jobprofilevacancy__score'))
        if hasattr(job_profile, 'preferences'):
            preferences = job_profile.preferences
            if preferences.industries.count():
                queryset = queryset.filter(industry__in=preferences.industries.all())
            if preferences.roles.count():
                queryset = queryset.filter(role__in=preferences.roles.all())
            if preferences.looking_for:
                queryset = queryset.filter(types__overlap=preferences.looking_for)
            if preferences.location:
                queryset = queryset.filter(location=preferences.location)
        return queryset

    def setUp(self):
        self.user = CandidateFactory()
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_return_401(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_return_vacancies_for_default_profile(self):
        vacancies = self.create_vacancies()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchVacancyPersonalizedSerializer(vacancies, many=True).data)
        self.assertEqual([vacancy for vacancy in vacancies], [
            self.vacancies[7],
            self.vacancies[4],
        ])

    def test_filter_selected_profile_should_return_rows(self):
        vacancies = self.create_vacancies(job_profile_idx=0)
        job_profile = self.job_profiles[0]
        response = self.client.get(self.url_with_querystring(self.list_url, **{
            'job_profile_id': job_profile.id,
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchVacancyPersonalizedSerializer(vacancies, many=True).data)
        self.assertEqual([vacancy for vacancy in vacancies], [
            self.vacancies[0],
        ])

    def test_filter_industry_and_types_in_selected_profile_should_return_200(self):
        vacancies = self.create_vacancies(job_profile_idx=2)
        vacancies = vacancies.filter(industry__in=[self.industries[0].id, self.industries[2].id])
        vacancies = vacancies.filter(types__overlap=[0, 2])
        job_profile = self.job_profiles[2]
        response = self.client.get(self.url_with_querystring(
            self.list_url,
            ('job_profile_id', job_profile.id,),
            ('industry_id', self.industries[0].id),
            ('industry_id', self.industries[2].id),
            ('types', 0),
            ('types', 2),
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), SearchVacancyPersonalizedSerializer(vacancies, many=True).data)
        self.assertEqual([vacancy for vacancy in vacancies], [
            self.vacancies[7],
            self.vacancies[6],
            self.vacancies[5],
            self.vacancies[3],
        ])

    def test_search_role_and_filter_industry_in_selected_profile_should_return_200(self):
        vacancies = self.create_vacancies(job_profile_idx=2)
        vacancies = vacancies.filter(role__name__icontains='free')
        job_profile = self.job_profiles[2]
        response = self.client.get(self.url_with_querystring(
            self.list_url,
            ('job_profile_id', job_profile.id,),
            ('industry_id', self.industries[2].id),
            ('industry_id', self.industries[0].id),
            ('role', 'free'),
        ))
        self.assertEqual(response.json().get('results'), SearchVacancyPersonalizedSerializer(vacancies, many=True).data)
        self.assertEqual([vacancy for vacancy in vacancies], [
            self.vacancies[7],
            self.vacancies[5],
            self.vacancies[3],
        ])

    def test_search_location_in_default_profile_should_return_list(self):
        search = 'den'
        vacancies = self.create_vacancies()
        vacancies = vacancies.filter(
            Q(location__city__name__icontains=search) | Q(location__state__name__icontains=search) | Q(
                location__country__name__icontains=search)
        )
        response = self.client.get(self.url_with_querystring(
            self.list_url,
            ('search', search),
        ))
        self.assertEqual(response.json().get('results'), SearchVacancyPersonalizedSerializer(vacancies, many=True).data)
        self.assertEqual([vacancy for vacancy in vacancies], [
            self.vacancies[7],
            self.vacancies[4],
        ])
