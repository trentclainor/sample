from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.user.serializers import UserSerializer
from sample.tests.factories import UserFactory


class UserTestCase(APITestCase):
    client_class = APIClient
    user = None

    def setUp(self):
        self.user = UserFactory.create()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

    def test_get_list_should_return_401(self):
        self.client.credentials()
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_return_current_user_rows(self):
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [UserSerializer(self.user).data])

    def test_get_current_user_data_should_return_current_user_data_dict(self):
        response = self.client.get(reverse('users-me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(self.user).data)

    def test_get_user_data_by_id_should_return_user_data_dict(self):
        response = self.client.get(reverse('users-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(self.user).data)

    def test_get_user_data_should_return_404(self):
        response = self.client.get(reverse('users-detail', args=[0]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
