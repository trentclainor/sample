from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sample.api.job_profile import serializers
from sample.job_profiles.models import JobProfile

User = get_user_model()


class JobProfileViewSet(ModelViewSet):
    """
    ViewSet for listing or retrieving job profiles
    """
    serializer_class = serializers.JobProfileSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated and self.request.user.is_candidate:
            return JobProfile.objects.filter(user=self.request.user)
        return JobProfile.objects.none()

    @detail_route(methods=['get', 'post'])
    def make_default(self, request, pk):
        job_profile = self.get_object()
        job_profile.is_default = True
        job_profile.save()
        return Response(serializers.JobProfileSerializer(job_profile).data, status=status.HTTP_200_OK)
