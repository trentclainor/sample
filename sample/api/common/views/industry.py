from rest_framework.viewsets import ReadOnlyModelViewSet

from sample.api.common import filters, serializers
from sample.common.models import Industry


class IndustryViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing industries
    """
    queryset = Industry.objects.all()
    serializer_class = serializers.IndustrySerializer
    search_fields = ('name',)
    filter_class = filters.IndustryFilter
