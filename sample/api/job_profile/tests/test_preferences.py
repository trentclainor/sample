from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.job_profile.serializers import PreferencesSerializer
from sample.job_profiles.models import Preferences
from sample.tests.factories import (IndustryFactory, JobProfileFactory, LocationFactory, PreferencesFactory,
                                       RoleFactory, UserFactory)


class PreferencesTestCase(APITestCase):
    client_class = APIClient
    user = None
    job_profile = None
    list_url = None
    detail_url = None
    industries = []
    location = None
    roles = []

    def setUp(self):
        self.user = UserFactory.create()
        self.job_profile = JobProfileFactory.create(user=self.user)
        self.industries = IndustryFactory.create_batch(3)
        self.location = LocationFactory.create()
        self.roles = RoleFactory.create_batch(3)
        self.list_url = reverse('job-profiles-preferences-list', args=[self.job_profile.id])
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_be_return_401(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_be_return_200(self):
        preferences = PreferencesFactory.create(job_profile=self.job_profile,
                                                industries=(self.industries[0], self.industries[2]),
                                                location=self.location,
                                                roles=(self.roles[0], self.roles[2]))
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [PreferencesSerializer(preferences).data])

    def test_get_should_be_return_200(self):
        preferences = PreferencesFactory.create(job_profile=self.job_profile,
                                                industries=(self.industries[0], self.industries[2]),
                                                roles=(self.roles[0], self.roles[2]))
        detail_url = reverse('job-profiles-preferences-detail', args=[self.job_profile.id, preferences.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), PreferencesSerializer(preferences).data)

    def test_post_should_be_return_201(self):
        response = self.client.post(self.list_url, {
            'location': self.location.id,
            'industries': [self.industries[0].id, self.industries[2].id],
            'roles': [self.roles[1].id],
            'looking_for': [0, 2],
            'weekly_email': False,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        preferences = Preferences.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), PreferencesSerializer(preferences).data)

    def test_post_if_wrong_location_should_be_return_400_with_error_message(self):
        response = self.client.post(self.list_url, {
            'location': 0
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('location', response.json())
        self.assertIn('Invalid pk "0" - object does not exist.', response.json().get('location'))

    def test_post_if_wrong_industries_roles_and_looking_for_string_location_should_be_return_400(self):
        response = self.client.post(self.list_url, {'industries': '', 'roles': '', 'location': 0, 'looking_for': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('industries', response.json())
        self.assertIn('Expected a list of items but got type "str".', response.json().get('industries'))
        self.assertIn('roles', response.json())
        self.assertIn('Expected a list of items but got type "str".', response.json().get('roles'))
        self.assertIn('location', response.json())
        self.assertIn('Invalid pk "0" - object does not exist.', response.json().get('location'))
        self.assertIn('looking_for', response.json())
        self.assertIn('Expected a list of items but got type "str".', response.json().get('looking_for'))

    def test_put_industries_roles_and_location_should_be_return_200(self):
        preferences = PreferencesFactory.create(job_profile=self.job_profile,
                                                industries=(self.industries[0], self.industries[2]),
                                                roles=(self.roles[0], self.roles[2]),
                                                location=LocationFactory.create())
        detail_url = reverse('job-profiles-preferences-detail', args=[self.job_profile.id, preferences.id])
        response = self.client.put(detail_url, {
            'industries': [self.industries[1].id],
            'roles': [self.roles[1].id],
            'location': self.location.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        preferences = Preferences.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), PreferencesSerializer(preferences).data)

    def test_put_if_looking_for_wrong_should_be_return_400_with_error_message(self):
        preferences = PreferencesFactory.create(job_profile=self.job_profile,
                                                industries=(self.industries[0], self.industries[2]),
                                                roles=(self.roles[0], self.roles[2]))
        detail_url = reverse('job-profiles-preferences-detail', args=[self.job_profile.id, preferences.id])
        response = self.client.put(detail_url, {
            'looking_for': ['new'],
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('looking_for', response.json())
        self.assertIn('"new" is not a valid choice.', response.json().get('looking_for'))

    def test_patch_should_be_return_200(self):
        preferences = PreferencesFactory.create(job_profile=self.job_profile,
                                                industries=(self.industries[0], self.industries[2]),
                                                roles=(self.roles[0], self.roles[2]))
        detail_url = reverse('job-profiles-preferences-detail', args=[self.job_profile.id, preferences.id])
        response = self.client.patch(detail_url, {
            'looking_for': [1, 2],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        preferences = Preferences.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), PreferencesSerializer(preferences).data)

    def test_patch_if_level_wrong_value_should_be_return_400_with_error_message(self):
        preferences = PreferencesFactory.create(job_profile=self.job_profile,
                                                industries=(self.industries[0], self.industries[2]),
                                                roles=(self.roles[0], self.roles[2]))
        detail_url = reverse('job-profiles-preferences-detail', args=[self.job_profile.id, preferences.id])
        response = self.client.patch(detail_url, {
            'looking_for': ['unknown'],
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('looking_for', response.json())
        self.assertIn('"unknown" is not a valid choice.', response.json().get('looking_for'))

    def test_delete_should_be_return_204(self):
        preferences = PreferencesFactory.create(job_profile=self.job_profile,
                                                industries=(self.industries[0], self.industries[2]),
                                                roles=(self.roles[0], self.roles[2]))
        detail_url = reverse('job-profiles-preferences-detail', args=[self.job_profile.id, preferences.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Preferences.objects.filter(id=preferences.id).exists())

    def test_delete_should_be_return_404(self):
        response = self.client.delete(reverse('job-profiles-preferences-detail', args=[self.job_profile.id, 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertIn('Not found.', response.json().get('detail'))

    def test_delete_should_be_return_403(self):
        user = UserFactory.create()
        job_profile = JobProfileFactory.create(user=user)
        preferences = PreferencesFactory.create(job_profile=job_profile)
        response = self.client.delete(reverse('job-profiles-preferences-detail', args=[job_profile.id, preferences.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())
        self.assertIn('You do not have permission to perform this action.', response.json().get('detail'))
