import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.test import RequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.user.serializers import CompanySerializer
from sample.tests.factories import CompanyFactory, UserFactory
from sample.users.models import Company


class CompanyTestCase(APITestCase):
    client_class = APIClient
    user = None
    companies = []
    list_url = None

    def setUp(self):
        self.user = UserFactory(is_recruiter=True)
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.list_url = reverse('users-companies-list', args=[self.user.id])

    def generate_image(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_get_list_should_return_401(self):
        self.client.credentials()
        response = self.client.get(reverse('users-companies-list', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_return_200(self):
        company = CompanyFactory(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [CompanySerializer(company).data])

    def test_get_should_return_200(self):
        company = CompanyFactory(user=self.user)
        response = self.client.get(reverse('users-companies-detail', args=[self.user.id, company.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), CompanySerializer(company).data)

    def test_post_should_return_201(self):
        response = self.client.post(self.list_url, {
            'name': 'new',
            'logo': self.generate_image(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        company = Company.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            CompanySerializer(company, context={'request': RequestFactory().get(self.list_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, company.logo.name))

    def test_post_if_name_empty_should_return_400_with_error_message(self):
        response = self.client.post(self.list_url, {
            'logo': BytesIO(b'1'),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        self.assertIn('logo', response.json())
        self.assertIn('Upload a valid image. The file you uploaded was either not an image or a corrupted image.',
                      response.json().get('logo'))

    def test_put_should_return_200(self):
        company = CompanyFactory(user=self.user)
        detail_url = reverse('users-companies-detail', args=[self.user.id, company.id])
        response = self.client.put(detail_url, {
            'name': 'updated',
            'logo': self.generate_image(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company = Company.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            CompanySerializer(company, context={'request': RequestFactory().get(detail_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, company.logo.name))

    def test_put_if_name_empty_should_return_400_with_error_message(self):
        company = CompanyFactory(user=self.user)
        detail_url = reverse('users-companies-detail', args=[self.user.id, company.id])
        response = self.client.put(detail_url, {
            'logo': BytesIO(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        self.assertIn('logo', response.json())
        self.assertIn('The submitted file is empty.', response.json().get('logo'))

    def test_patch_should_return_200(self):
        company = CompanyFactory(user=self.user)
        detail_url = reverse('users-companies-detail', args=[self.user.id, company.id])
        response = self.client.patch(detail_url, {
            'logo': self.generate_image(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company = Company.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            CompanySerializer(company, context={'request': RequestFactory().get(detail_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, company.logo.name))

    def test_patch_if_logo_wrong_value_should_return_400_with_error_message(self):
        company = CompanyFactory(user=self.user)
        detail_url = reverse('users-companies-detail', args=[self.user.id, company.id])
        response = self.client.patch(detail_url, {
            'logo': BytesIO(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('logo', response.json())
        self.assertIn('The submitted file is empty.', response.json().get('logo'))

    def test_delete_should_return_204(self):
        company = CompanyFactory(user=self.user)
        response = self.client.delete(reverse('users-companies-detail', args=[self.user.id, company.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company.id).exists())

    def test_delete_should_return_404(self):
        response = self.client.delete(reverse('users-companies-detail', args=[self.user.id, 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
