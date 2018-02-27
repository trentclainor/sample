from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.tests.factories import UserFactory


class AuthTestCase(APITestCase):
    client_class = APIClient
    password = '12345678abc'
    url = reverse('auth-token')
    user = None

    def setUp(self):
        self.user = UserFactory(password=self.password)

    def test_post_login_and_password_should_return_token(self):
        response = self.client.post(self.url, {
            'username': self.user.email,
            'password': self.password,
        })
        token = Token.objects.get(user__pk=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('token'), token.key)

    def test_post_empty_data_should_return_error_message(self):
        response = self.client.post(self.url)
        self.assertIn('username', response.json())
        self.assertIn('This field is required.', response.json().get('username'))
        self.assertIn('password', response.json())
        self.assertIn('This field is required.', response.json().get('password'))

    def test_post_blank_data_should_return_error_message(self):
        response = self.client.post(self.url, {
            'username': '',
            'password': '',
        })
        self.assertIn('username', response.json())
        self.assertIn('This field may not be blank.', response.json().get('username'))
        self.assertIn('password', response.json())
        self.assertIn('This field may not be blank.', response.json().get('password'))

    def test_post_wrong_password_should_return_error(self):
        response = self.client.post(self.url, {
            'username': self.user.email,
            'password': self.password + 'abc',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())
        self.assertIn('Unable to log in with provided credentials.', response.json().get('non_field_errors'))

    def test_post_wrong_login_or_password_should_return_error(self):
        response = self.client.post(self.url, {
            'username': 'username',
            'password': 'password',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())
        self.assertIn('Unable to log in with provided credentials.', response.json().get('non_field_errors'))
