from django.contrib.auth import get_user_model

from sample.api.base_viewset import NestedModelViewSet
from sample.api.user import serializers
from sample.users.models import Company

User = get_user_model()


class CompanyViewSet(NestedModelViewSet):
    serializer_class = serializers.CompanySerializer
    parent_lookup = 'user'

    def get_parent_queryset(self):
        if self.request.user and self.request.user.is_authenticated and self.request.user.is_recruiter:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_queryset(self):
        if self.request.user:
            return Company.objects.filter(user=self.request.user)
        return Company.objects.none()
