from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.user.serializers import CandidateSerializer, UserSerializer
from sample.tests.factories import UserFactory

User = get_user_model()


class CandidateTestCase(APITestCase):
    client_class = APIClient
    user = None

    url = reverse('users-candidate-register')

    def test_get_should_return_405(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_user_data_should_register_candidate_and_return_token(self):
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'name': 'Name',
            'password': '12345678',
        })
        self.assertIn('token', response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(auth_token=response.json().get('token', 0))
        serializer_data = CandidateSerializer(user).data
        serializer_data.update({'token': user.auth_token.key})
        self.assertEqual(response.json(), serializer_data)
        self.assertTrue(user.is_candidate)

    def test_user_auth_after_register_should_return_user_info(self):
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'name': 'Name',
            'password': '12345678',
        })
        self.assertIn('token', response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(auth_token=response.json().get('token', 0))
        serializer_data = CandidateSerializer(user).data
        serializer_data.update({'token': user.auth_token.key})
        self.assertEqual(response.json(), serializer_data)
        self.assertTrue(user.is_candidate)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        response = self.client.get(reverse('users-me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(user).data)

    def test_post_exists_email_should_return_error_with_message(self):
        user = UserFactory(is_candidate=True)
        response = self.client.post(self.url, {
            'email': user.email,
            'name': 'Name',
            'password': '12345678',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())
        self.assertIn('user with this email address already exists.', response.json().get('email'))

    def test_post_empty_data_should_return_error_with_message(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())
        self.assertIn('This field is required.', response.json().get('email'))
        self.assertIn('password', response.json())
        self.assertIn('This field is required.', response.json().get('password'))

    def test_post_blank_data_should_return_error_with_message(self):
        response = self.client.post(self.url, {
            'email': '',
            'password': '',
            'name': '',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.json())
        self.assertIn('This field may not be blank.', response.json().get('email'))
        self.assertIn('password', response.json())
        self.assertIn('This field may not be blank.', response.json().get('password'))
        self.assertIn('name', response.json())
        self.assertIn('This field may not be blank.', response.json().get('name'))
