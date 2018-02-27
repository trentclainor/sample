import os
from io import BytesIO

from django.conf import settings
from django.test import RequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.job_profile.serializers import JobProfileSerializer
from sample.job_profiles.models import JobProfile
from sample.tests.factories import CandidateFactory, JobProfileFactory, UserFactory


class JobProfileTestCase(APITestCase):
    client_class = APIClient
    user = None
    job_profiles = []

    def setUp(self):
        users = CandidateFactory.create_batch(5)
        self.user = users[1]
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_be_return_401(self):
        self.client.credentials()
        response = self.client.get(reverse('job-profiles-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_be_return_200(self):
        job_profile = JobProfileFactory.create(user=self.user)
        response = self.client.get(reverse('job-profiles-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [JobProfileSerializer(job_profile).data])

    def test_get_should_be_return_200(self):
        job_profile = JobProfileFactory.create(user=self.user)
        response = self.client.get(reverse('job-profiles-detail', args=[job_profile.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), JobProfileSerializer(job_profile).data)

    def test_make_default_job_profile_should_be_return_200(self):
        job_profile1 = JobProfileFactory.create(user=self.user, is_default=True)
        job_profile2 = JobProfileFactory.create(user=self.user, is_default=True)
        job_profile = JobProfileFactory.create(user=self.user)
        response = self.client.get(reverse('job-profiles-make-default', args=[job_profile.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job_profile = JobProfile.objects.get(id=response.json().get('id', 0))
        self.assertTrue(JobProfileSerializer(job_profile).data['is_default'])
        job_profile = JobProfile.objects.get(id=job_profile1.id)
        self.assertFalse(JobProfileSerializer(job_profile).data['is_default'])
        job_profile = JobProfile.objects.get(id=job_profile2.id)
        self.assertFalse(JobProfileSerializer(job_profile).data['is_default'])

    def test_post_should_be_return_201(self):
        file = BytesIO(b'1')
        file.name = 'example.pdf'
        list_url = reverse('job-profiles-list')
        response = self.client.post(list_url, {
            'name': 'new',
            'cv': file,
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        job_profile = JobProfile.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            JobProfileSerializer(job_profile, context={'request': RequestFactory().get(list_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, job_profile.cv.name))

    def test_post_job_profiles_is_default_old_profile_is_default_should_be_false_should_be_return_201(self):
        list_url = reverse('job-profiles-list')
        job_profile1 = JobProfileFactory.create(user=self.user, is_default=True)
        job_profile2 = JobProfileFactory.create(user=self.user, is_default=True)
        response = self.client.post(list_url, {
            'name': 'new',
            'is_default': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        job_profile = JobProfile.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            JobProfileSerializer(job_profile).data
        )
        job_profile = JobProfile.objects.get(id=job_profile1.id)
        self.assertFalse(JobProfileSerializer(job_profile).data['is_default'])
        job_profile = JobProfile.objects.get(id=job_profile2.id)
        self.assertFalse(JobProfileSerializer(job_profile).data['is_default'])

    def test_post_if_name_empty_should_be_return_400_with_error_message(self):
        list_url = reverse('job-profiles-list')
        response = self.client.post(list_url, {
            'cv': BytesIO(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        self.assertIn('cv', response.json())
        self.assertIn('The submitted file is empty.', response.json().get('cv'))

    def test_put_should_be_return_200(self):
        job_profile = JobProfileFactory.create(user=self.user)
        file = BytesIO(b'2')
        file.name = 'example.pdf'
        detail_url = reverse('job-profiles-detail', args=[job_profile.id])
        response = self.client.put(detail_url, {
            'name': 'updated',
            'cv': file,
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job_profile = JobProfile.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            JobProfileSerializer(job_profile, context={'request': RequestFactory().get(detail_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, job_profile.cv.name))

    def test_put_if_name_empty_should_be_return_400_with_error_message(self):
        job_profile = JobProfileFactory.create(user=self.user)
        detail_url = reverse('job-profiles-detail', args=[job_profile.id])
        response = self.client.put(detail_url, {
            'cv': BytesIO(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        self.assertIn('cv', response.json())
        self.assertIn('The submitted file is empty.', response.json().get('cv'))

    def test_patch_should_be_return_200(self):
        job_profile = JobProfileFactory.create(user=self.user)
        file = BytesIO(b'3')
        file.name = 'example.pdf'
        detail_url = reverse('job-profiles-detail', args=[job_profile.id])
        response = self.client.patch(detail_url, {
            'cv': file,
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job_profile = JobProfile.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            JobProfileSerializer(job_profile, context={'request': RequestFactory().get(detail_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, job_profile.cv.name))

    def test_patch_is_default_should_reset_to_false_another_job_profiles_should_be_return_200(self):
        job_profile1 = JobProfileFactory.create(user=self.user, is_default=True)
        job_profile2 = JobProfileFactory.create(user=self.user)
        job_profile = JobProfileFactory.create(user=self.user)
        detail_url = reverse('job-profiles-detail', args=[job_profile.id])
        response = self.client.patch(detail_url, {
            'is_default': True,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job_profile = JobProfile.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            JobProfileSerializer(job_profile).data
        )
        job_profile = JobProfile.objects.get(id=job_profile1.id)
        self.assertFalse(JobProfileSerializer(job_profile).data['is_default'])
        job_profile = JobProfile.objects.get(id=job_profile2.id)
        self.assertFalse(JobProfileSerializer(job_profile).data['is_default'])

    def test_patch_if_cv_wrong_value_should_be_return_400_with_error_message(self):
        job_profile = JobProfileFactory.create(user=self.user)
        detail_url = reverse('job-profiles-detail', args=[job_profile.id])
        response = self.client.patch(detail_url, {
            'cv': BytesIO(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cv', response.json())
        self.assertIn('The submitted file is empty.', response.json().get('cv'))

    def test_delete_should_be_return_204(self):
        job_profile = JobProfileFactory.create(user=self.user)
        response = self.client.delete(reverse('job-profiles-detail', args=[job_profile.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobProfile.objects.filter(id=job_profile.id).exists())

    def test_delete_should_be_return_404(self):
        response = self.client.delete(reverse('job-profiles-detail', args=[1]))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertIn('Not found.', response.json().get('detail'))
        self.assertFalse(JobProfile.objects.filter(id=1).exists())

    def test_delete_exists_another_user_should_be_return_403(self):
        user = UserFactory.create()
        job_profile = JobProfileFactory.create(user=user)
        response = self.client.delete(reverse('job-profiles-detail', args=[job_profile.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(JobProfile.objects.filter(id=job_profile.id).exists())
