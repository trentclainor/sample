import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.test import RequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from sample.api.job_profile.serializers import BasicInfoSerializer
from sample.job_profiles.models import BasicInfo
from sample.tests.factories import BasicInfoFactory, JobProfileFactory, UserFactory


class BasicInfoTestCase(APITestCase):
    client_class = APIClient
    user = None
    job_profile = None
    list_url = None
    detail_url = None

    def setUp(self):
        users = UserFactory.create_batch(5)
        self.user = users[1]
        job_profiles = JobProfileFactory.create_batch(5, user=self.user)
        self.job_profile = job_profiles[1]
        self.list_url = reverse('job-profiles-basic-info-list', args=[self.job_profile.id])
        token = Token.objects.get(user__pk=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def generate_photo_file(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_get_list_should_be_return_401(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_should_be_return_200(self):
        basic_info = BasicInfoFactory.create(job_profile=self.job_profile)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), [BasicInfoSerializer(basic_info).data])

    def test_get_should_be_return_200(self):
        basic_info = BasicInfoFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-basic-info-detail', args=[self.job_profile.id, basic_info.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), BasicInfoSerializer(basic_info).data)

    def test_post_should_be_return_201(self):
        response = self.client.post(self.list_url, {
            'name': 'new',
            'photo': self.generate_photo_file(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        basic_info = BasicInfo.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            BasicInfoSerializer(basic_info, context={'request': RequestFactory().get(self.list_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, basic_info.photo.name))

    def test_post_if_name_empty_should_be_return_400_with_error_message(self):
        response = self.client.post(self.list_url, {
            'photo': BytesIO(b'1'),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        self.assertIn('photo', response.json())
        self.assertIn('Upload a valid image. The file you uploaded was either not an image or a corrupted image.',
                      response.json().get('photo'))

    def test_put_should_be_return_200(self):
        basic_info = BasicInfoFactory.create(job_profile=self.job_profile)
        file = BytesIO(b'2')
        file.name = 'example.pdf'
        detail_url = reverse('job-profiles-basic-info-detail', args=[self.job_profile.id, basic_info.id])
        response = self.client.put(detail_url, {
            'name': 'updated',
            'photo': self.generate_photo_file(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        basic_info = BasicInfo.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            BasicInfoSerializer(basic_info, context={'request': RequestFactory().get(detail_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, basic_info.photo.name))

    def test_put_if_name_empty_should_be_return_400_with_error_message(self):
        basic_info = BasicInfoFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-basic-info-detail', args=[self.job_profile.id, basic_info.id])
        response = self.client.put(detail_url, {
            'photo': BytesIO(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json())
        self.assertIn('This field is required.', response.json().get('name'))
        self.assertIn('photo', response.json())
        self.assertIn('The submitted file is empty.', response.json().get('photo'))

    def test_patch_should_be_return_200(self):
        basic_info = BasicInfoFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-basic-info-detail', args=[self.job_profile.id, basic_info.id])
        response = self.client.patch(detail_url, {
            'photo': self.generate_photo_file(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        basic_info = BasicInfo.objects.get(id=response.json().get('id', 0))
        self.assertEqual(
            response.json(),
            BasicInfoSerializer(basic_info, context={'request': RequestFactory().get(detail_url)}).data
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, basic_info.photo.name))

    def test_patch_if_photo_wrong_value_should_be_return_400_with_error_message(self):
        basic_info = BasicInfoFactory.create(job_profile=self.job_profile)
        detail_url = reverse('job-profiles-basic-info-detail', args=[self.job_profile.id, basic_info.id])
        response = self.client.patch(detail_url, {
            'photo': BytesIO(),
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('photo', response.json())
        self.assertIn('The submitted file is empty.', response.json().get('photo'))

    def test_delete_should_be_return_204(self):
        basic_info = BasicInfoFactory.create(job_profile=self.job_profile)
        response = self.client.delete(
            reverse('job-profiles-basic-info-detail', args=[self.job_profile.id, basic_info.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BasicInfo.objects.filter(id=basic_info.id).exists())

    def test_delete_should_be_return_404(self):
        self.assertFalse(BasicInfo.objects.filter(id=1).exists())
        response = self.client.delete(reverse('job-profiles-basic-info-detail', args=[self.job_profile.id, 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertIn('Not found.', response.json().get('detail'))

    def test_delete_should_be_return_403(self):
        user = UserFactory.create()
        job_profile = JobProfileFactory.create(user=user)
        basic_info = BasicInfoFactory.create(job_profile=job_profile)
        response = self.client.delete(reverse('job-profiles-basic-info-detail', args=[job_profile.id, basic_info.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())
        self.assertIn('You do not have permission to perform this action.', response.json().get('detail'))
