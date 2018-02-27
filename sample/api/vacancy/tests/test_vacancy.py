from django.db.models import Count
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.vacancy.serializers import VacancySerializer
from sample.tests.factories import (CityFactory, CompanyFactory, CountryFactory, IndustryFactory, LocationFactory,
                                       RecruiterFactory, RoleFactory, VacancyFactory)
from sample.vacancies.models import Vacancy


class VacancyTestCase(APITestCase):
    client_class = APIClient
    maxDiff = None
    user = None
    company = None
    list_url = None
    detail_url = None
    industries = []
    locations = []
    vacancies = []

    def create_vacancies(self):
        countries = [
            CountryFactory(name='UK'),
        ]
        cities = [
            CityFactory(name='London'),
        ]
        self.locations = l = [
            LocationFactory(country=countries[0]),
            LocationFactory(country=countries[0], city=cities[0]),
        ]
        self.industries = i = IndustryFactory.create_batch(3)

        self.roles = r = RoleFactory.create_batch(3)
        users = [
            self.user,
            RecruiterFactory(),
        ]
        self.companies = c = [
            self.company,
            CompanyFactory(user=users[1]),
        ]
        self.vacancies = [
            VacancyFactory(location=l[0], company=c[0]),
            VacancyFactory(location=l[1], company=c[1]),
            VacancyFactory(location=l[1], company=c[0]),
        ]
        return Vacancy.objects.filter(company__user=self.user).annotate(
            matches=Count('jobprofilevacancy__job_profile'))

    def create_vacancy(self):
        # VacancyFactory(company=self.company)
        # return Vacancy.objects.filter(company__user=self.user).annotate(
        #     matches=Count('jobprofilevacancy__job_profile')).first()
        return VacancyFactory(company=self.company)

    def setUp(self):
        self.user = RecruiterFactory()
        self.company = CompanyFactory(user=self.user)
        self.list_url = reverse('vacancies-list')
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_return_401(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_return_all_rows(self):
        vacancies = self.create_vacancies()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), VacancySerializer(vacancies, many=True).data)

    def test_get_by_id_should_return_row(self):
        vacancies = self.create_vacancies()
        detail_url = reverse('vacancies-detail', args=[vacancies[0].id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = VacancySerializer(vacancies[0]).data
        self.assertEqual(response.json(), serializer_data)

    def test_post_should_create_row(self):
        response = self.client.post(self.list_url, {
            'name': 'new name',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vacancy = Vacancy.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), VacancySerializer(vacancy).data)

    def test_post_if_name_empty_should_return_400_with_error_message(self):
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))

    def test_put_should_update_row(self):
        vacancy = self.create_vacancy()
        detail_url = reverse('vacancies-detail', args=[vacancy.id])
        response = self.client.put(detail_url, {
            'name': 'updated',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vacancy = Vacancy.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), VacancySerializer(vacancy).data)

    def test_put_if_name_empty_should_return_400_with_error_message(self):
        vacancy = self.create_vacancy()
        detail_url = reverse('vacancies-detail', args=[vacancy.id])
        response = self.client.put(detail_url, {
            'descr': 'new decription',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        # self.assertIn('company', response.json())
        # self.assertIn('This field is required.', response.json().get('company'))

    def test_patch_should_update_row(self):
        vacancy = self.create_vacancy()
        detail_url = reverse('vacancies-detail', args=[vacancy.id])
        response = self.client.patch(detail_url, {
            'name': 'updated',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vacancy = Vacancy.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), VacancySerializer(vacancy).data)

    def test_patch_if_types_contains_wrong_value_should_return_400_with_error_message(self):
        vacancy = self.create_vacancy()
        detail_url = reverse('vacancies-detail', args=[vacancy.id])
        response = self.client.patch(detail_url, {
            'types': [1, 2, 3, 4, 5],
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('types', response.json())
        self.assertIn('"5" is not a valid choice.', response.json().get('types'))

    def test_delete_should_delete_row(self):
        vacancy = self.create_vacancy()
        detail_url = reverse('vacancies-detail', args=[vacancy.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vacancy.objects.filter(id=vacancy.id).exists())

    def test_delete_not_exists_should_return_404(self):
        self.create_vacancies()
        response = self.client.delete(reverse('vacancies-detail', args=[self.vacancies[1].id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertIn('Not found.', response.json().get('detail'))
