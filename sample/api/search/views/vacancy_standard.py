from rest_framework.viewsets import ReadOnlyModelViewSet

from sample.api.permissions import IsCandidate
from sample.api.search import serializers
from sample.vacancies.models import Vacancy
from ..filters import FilterSearchVacancyStandard


class SearchVacancyStandardViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for search standard vacancies
    """

    serializer_class = serializers.SearchVacancyStandardSerializer
    search_fields = ('location__city__name', 'location__state__name', 'location__country__name')
    filter_class = FilterSearchVacancyStandard
    permission_classes = (IsCandidate,)
    ordering = ('-modified',)

    def get_queryset(self):
        queryset = Vacancy.objects.select_related('location', 'location__city', 'location__country', 'industry',
                                                  'company', 'company__user', 'role').all()
        return queryset
