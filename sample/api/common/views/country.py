from rest_framework.viewsets import ReadOnlyModelViewSet

from sample.api.common import filters, serializers
from sample.common.models import Country


class CountryViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing countries
    """
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer
    search_fields = ('name',)
    filter_class = filters.CountryFilter
