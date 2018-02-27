from django.contrib.auth import get_user_model

from sample.api.base_viewset import NestedModelViewSet
from sample.api.job_profile import serializers
from sample.job_profiles.models import JobProfile, Preferences

User = get_user_model()


class PreferencesViewSet(NestedModelViewSet):
    serializer_class = serializers.PreferencesSerializer
    parent_lookup = 'job_profile'

    def get_parent_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            return JobProfile.objects.filter(user=self.request.user)
        return JobProfile.objects.none()

    def get_queryset(self):
        if self.is_valid_parent_pk():
            return Preferences.objects.filter(job_profile_id=self.parent_pk)
        return Preferences.objects.none()
