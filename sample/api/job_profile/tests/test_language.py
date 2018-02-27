from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.job_profile.serializers import LanguageSerializer
from sample.job_profiles.models import LANG_LEVELS, Language
from sample.tests.factories import JobProfileFactory, LanguageFactory, UserFactory


class LanguageTestCase(APITestCase):
    client_class = APIClient
    user = None
    job_profile = None
    list_url = None
    detail_url = None

    def setUp(self):
        self.user = UserFactory.create()
        self.job_profile = JobProfileFactory.create(user=self.user)
        self.list_url = reverse('job-profiles-languages-list', args=[self.job_profile.id])
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_be_return_401(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_be_return_200(self):
        language = LanguageFactory.create(job_profile=self.job_profile)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [LanguageSerializer(language).data])

    def test_get_should_be_return_200(self):
        language = LanguageFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-languages-detail', args=[self.job_profile.id, language.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), LanguageSerializer(language).data)

    def test_post_should_be_return_201(self):
        response = self.client.post(self.list_url, {
            'name': 'Thai',
            'level': LANG_LEVELS.basic,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        language = Language.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), LanguageSerializer(language).data)

    def test_post_if_name_empty_should_be_return_400_with_error_message(self):
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))

    def test_put_should_be_return_200(self):
        language = LanguageFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-languages-detail', args=[self.job_profile.id, language.id])
        response = self.client.put(detail_url, {
            'name': 'updated',
            'level': LANG_LEVELS.fluent,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        language = Language.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), LanguageSerializer(language).data)

    def test_put_if_name_empty_should_be_return_400_with_error_message(self):
        language = LanguageFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-languages-detail', args=[self.job_profile.id, language.id])
        response = self.client.put(detail_url, {
            'level': 'unknown',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        self.assertIn('level', response.json())
        self.assertIn('"unknown" is not a valid choice.', response.json().get('level'))

    def test_patch_should_be_return_200(self):
        language = LanguageFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-languages-detail', args=[self.job_profile.id, language.id])
        response = self.client.patch(detail_url, {
            'name': 'update',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        language = Language.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), LanguageSerializer(language).data)

    def test_patch_if_level_wrong_value_should_be_return_400_with_error_message(self):
        language = LanguageFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-languages-detail', args=[self.job_profile.id, language.id])
        response = self.client.patch(detail_url, {
            'level': 'unknown',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('level', response.json())
        self.assertIn('"unknown" is not a valid choice.', response.json().get('level'))

    def test_delete_should_be_return_204(self):
        language = LanguageFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-languages-detail', args=[self.job_profile.id, language.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Language.objects.filter(id=language.id).exists())

    def test_delete_should_be_return_404(self):
        self.assertFalse(Language.objects.filter(id=1).exists())
        response = self.client.delete(reverse('job-profiles-languages-detail', args=[self.job_profile.id, 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertIn('Not found.', response.json().get('detail'))

    def test_delete_should_be_return_403(self):
        user = UserFactory.create()
        job_profile = JobProfileFactory.create(user=user)
        language = LanguageFactory.create(job_profile=job_profile)
        response = self.client.delete(reverse('job-profiles-languages-detail', args=[job_profile.id, language.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())
        self.assertIn('You do not have permission to perform this action.', response.json().get('detail'))
