from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet

from sample.api.permissions import IsRecruiter
from sample.api.vacancy import serializers
from sample.vacancies.models import Vacancy

User = get_user_model()


class VacancyViewSet(ModelViewSet):
    """ViewSet for listing or retrieving jobs"""
    serializer_class = serializers.VacancySerializer
    parent_queryset = None
    permission_classes = (IsRecruiter,)

    def get_queryset(self):
        return Vacancy.objects.filter(company__user=self.request.user).annotate(
            matches=Count('jobprofilevacancy__job_profile'))
