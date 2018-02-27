import urllib.parse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.search.serializers import SearchVacancyStandardSerializer
from sample.tests.factories import (CandidateFactory, CityFactory, CountryFactory, IndustryFactory, LocationFactory,
                                       StateFactory, VacancyFactory)


class SearchVacancyStandardTestCase(APITestCase):
    client_class = APIClient
    user = None
    vacancies = []
    industries = []
    locations = []
    maxDiff = None

    def url_with_querystring(self, path, *args, **kwargs):
        if args:
            return '{}?{}'.format(path, urllib.parse.urlencode(args, doseq=True))
        return '{}?{}'.format(path, urllib.parse.urlencode(kwargs))

    def create_vacancies(self):
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
        self.locations = [
            LocationFactory(country=countries[0], state=states[0], city=cities[0]),  # 0, Maidstone, Kent, UK
            LocationFactory(country=countries[0], state=None, city=cities[1]),  # 1, London, UK
            LocationFactory(country=countries[0], state=None, city=None),  # 2, UK
            LocationFactory(country=countries[1], state=states[1], city=cities[2]),  # 3, Phoenix, Arizona, USA
            LocationFactory(country=countries[1], state=None, city=cities[3]),  # 4, Denver, USA
            LocationFactory(country=countries[1], state=None, city=None),  # 5, USA
        ]
        self.industries = [
            IndustryFactory(name='Finance'),  # 0
            IndustryFactory(name='Freelance'),  # 1
            IndustryFactory(name='Medicine'),  # 2
            IndustryFactory(name='Education'),  # 3
            IndustryFactory(name='Entertainment'),  # 4
        ]
        self.vacancies = [
            VacancyFactory(name='Vacancy 1 s1', location=self.locations[0], industry=self.industries[0], types=[0]),
            VacancyFactory(name='Vacancy 2', location=self.locations[1], industry=self.industries[1], types=[1]),
            VacancyFactory(name='Vacancy 3 ', location=self.locations[2], industry=self.industries[1], types=[0, 1]),
            VacancyFactory(name='Vacancy 4', location=self.locations[3], industry=self.industries[2], types=[1, 2]),
            VacancyFactory(name='Vacancy 5 s3', location=self.locations[4], industry=self.industries[3], types=[0, 1]),
            VacancyFactory(name='Vacancy 6', location=self.locations[3], industry=self.industries[3], types=[0, 2]),
            VacancyFactory(name='Vacancy 7 s2', location=self.locations[2], industry=self.industries[4],
                           types=[1, 2, 3]),
            VacancyFactory(name='Vacancy 8', location=self.locations[5], industry=self.industries[4], types=[1, 3]),
        ]

    def setUp(self):
        self.user = CandidateFactory.create()
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_return_401(self):
        self.client.credentials()
        response = self.client.get(reverse('search-vacancies-standard-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_return_all_rows(self):
        country = CountryFactory.create(name='UK')
        city = CityFactory.create(name='London')
        location = LocationFactory.create(country=country, city=city)
        vacancy = VacancyFactory.create(location=location)
        response = self.client.get(reverse('search-vacancies-standard-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [SearchVacancyStandardSerializer(vacancy).data])

    def test_filter_with_name_query_should_apply_name_filter_on_results(self):
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(reverse('search-vacancies-standard-list'), **{
            'types': 0,
            'ordering': 'id',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [
            SearchVacancyStandardSerializer(self.vacancies[0]).data,
            SearchVacancyStandardSerializer(self.vacancies[2]).data,
            SearchVacancyStandardSerializer(self.vacancies[4]).data,
            SearchVacancyStandardSerializer(self.vacancies[5]).data,
        ])

    def test_filter_with_types_should_apply_types_filter_on_results(self):
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(
            reverse('search-vacancies-standard-list'),
            ('types', 2),
            ('types', 3),
            ('ordering', '-modified')
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [
            SearchVacancyStandardSerializer(self.vacancies[7]).data,
            SearchVacancyStandardSerializer(self.vacancies[6]).data,
            SearchVacancyStandardSerializer(self.vacancies[5]).data,
            SearchVacancyStandardSerializer(self.vacancies[3]).data,
        ])

    def test_filter_name_should_apply_name_filter_on_results(self):
        """Filter name"""
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(reverse('search-vacancies-standard-list'), **{
            'name': 's',
            'ordering': 'name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [
            SearchVacancyStandardSerializer(self.vacancies[0]).data,
            SearchVacancyStandardSerializer(self.vacancies[4]).data,
            SearchVacancyStandardSerializer(self.vacancies[6]).data,
        ])

    def test_filter_industry_should_apply_industry_filter_on_results(self):
        """ Filter Medicine and Education """
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(reverse('search-vacancies-standard-list'), **{
            'industry': 'ed',
            'ordering': '-name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [
            SearchVacancyStandardSerializer(self.vacancies[5]).data,
            SearchVacancyStandardSerializer(self.vacancies[4]).data,
            SearchVacancyStandardSerializer(self.vacancies[3]).data,
        ])

    def test_search_location_should_search_rows_with_locations(self):
        """ Search Kent, Phoenix, Denver """
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(reverse('search-vacancies-standard-list'), **{
            'search': 'en',
            'ordering': 'name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [
            SearchVacancyStandardSerializer(self.vacancies[0]).data,
            SearchVacancyStandardSerializer(self.vacancies[3]).data,
            SearchVacancyStandardSerializer(self.vacancies[4]).data,
            SearchVacancyStandardSerializer(self.vacancies[5]).data,
        ])

    def test_ordering_should_apply_ordering_to_rows(self):
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(reverse('search-vacancies-standard-list'), **{
            'ordering': '-name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [
            SearchVacancyStandardSerializer(self.vacancies[7]).data,
            SearchVacancyStandardSerializer(self.vacancies[6]).data,
            SearchVacancyStandardSerializer(self.vacancies[5]).data,
            SearchVacancyStandardSerializer(self.vacancies[4]).data,
            SearchVacancyStandardSerializer(self.vacancies[3]).data,
            SearchVacancyStandardSerializer(self.vacancies[2]).data,
            SearchVacancyStandardSerializer(self.vacancies[1]).data,
            SearchVacancyStandardSerializer(self.vacancies[0]).data,
        ])

    def test_filter_with_search_industry_should_apply_filter_and_search(self):
        """ Filter Medicine and Education in USA on full time"""
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(reverse('search-vacancies-standard-list'), **{
            'industry': 'ed',
            'search': 'USA',
            'types': '1',
            'ordering': '-name',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [
            SearchVacancyStandardSerializer(self.vacancies[4]).data,
            SearchVacancyStandardSerializer(self.vacancies[3]).data,
        ])

    def test_filter_with_wrong_types_should_return_400(self):
        self.create_vacancies()
        response = self.client.get(self.url_with_querystring(reverse('search-vacancies-standard-list'), **{
            'types': 's',
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
