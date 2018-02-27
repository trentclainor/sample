import datetime

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.job_profile.serializers import EducationSerializer
from sample.job_profiles.models import Education
from sample.tests.factories import EducationFactory, JobProfileFactory, UserFactory


class EducationTestCase(APITestCase):
    client_class = APIClient
    user = None
    job_profile = None
    list_url = None
    detail_url = None

    def setUp(self):
        self.user = UserFactory.create()
        self.job_profile = JobProfileFactory.create(user=self.user)
        self.list_url = reverse('job-profiles-educations-list', args=[self.job_profile.id])
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_list_should_be_return_401(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_be_return_200(self):
        education = EducationFactory.create(job_profile=self.job_profile)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [EducationSerializer(education).data])

    def test_get_should_be_return_200(self):
        education = EducationFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-educations-detail', args=[self.job_profile.id, education.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), EducationSerializer(education).data)

    def test_post_should_be_return_201(self):
        response = self.client.post(self.list_url, {
            'school': 'MiT',
            'degree': 'Bachelor',
            'start_date': datetime.date(2002, 11, 1),
            'end_date': datetime.date(2003, 11, 30)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        education = Education.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), EducationSerializer(education).data)

    def test_post_if_name_empty_should_be_return_400_with_error_message(self):
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('school', response.json())
        self.assertIn('This field is required.', response.json().get('school'))
        self.assertIn('degree', response.json())
        self.assertIn('This field is required.', response.json().get('degree'))
        self.assertIn('start_date', response.json())
        self.assertIn('This field is required.', response.json().get('start_date'))

    def test_put_should_be_return_200(self):
        education = EducationFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-educations-detail', args=[self.job_profile.id, education.id])
        response = self.client.put(detail_url, {
            'school': 'updated',
            'degree': 'updated',
            'start_date': datetime.date(2003, 11, 1),
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        education = Education.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), EducationSerializer(education).data)

    def test_put_if_name_empty_should_be_return_400_with_error_message(self):
        education = EducationFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-educations-detail', args=[self.job_profile.id, education.id])
        response = self.client.put(detail_url, {
            'start_date': '2003-13-32',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('school', response.json())
        self.assertIn('This field is required.', response.json().get('school'))
        self.assertIn('degree', response.json())
        self.assertIn('This field is required.', response.json().get('degree'))
        self.assertIn('start_date', response.json())
        self.assertIn('Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].',
                      response.json().get('start_date'))

    def test_patch_should_be_return_200(self):
        education = EducationFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-educations-detail', args=[self.job_profile.id, education.id])
        response = self.client.patch(detail_url, {
            'degree': 'update',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        education = Education.objects.get(id=response.json().get('id', 0))
        self.assertEqual(response.json(), EducationSerializer(education).data)

    def test_patch_if_start_date_wrong_value_should_be_return_400_with_error_message(self):
        education = EducationFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-educations-detail', args=[self.job_profile.id, education.id])
        response = self.client.patch(detail_url, {
            'start_date': '2003-13-32',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date', response.json())
        self.assertIn('Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].',
                      response.json().get('start_date'))

    def test_delete_should_be_return_204(self):
        education = EducationFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-educations-detail', args=[self.job_profile.id, education.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(id=education.id).exists())

    def test_delete_should_be_return_404(self):
        self.assertFalse(Education.objects.filter(id=1).exists())
        response = self.client.delete(reverse('job-profiles-educations-detail', args=[self.job_profile.id, 1]))
        self.assertIn('detail', response.json())
        self.assertIn('Not found.', response.json().get('detail'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_should_be_return_403(self):
        user = UserFactory.create()
        job_profile = JobProfileFactory.create(user=user)
        education = EducationFactory.create(job_profile=job_profile)
        response = self.client.delete(reverse('job-profiles-educations-detail', args=[job_profile.id, education.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())
        self.assertIn('You do not have permission to perform this action.', response.json().get('detail'))
