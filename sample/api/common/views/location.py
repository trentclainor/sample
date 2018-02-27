from rest_framework.viewsets import ReadOnlyModelViewSet

from sample.api.common import filters, serializers
from sample.common.models import Location


class LocationViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing locations
    """
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    search_fields = ('country__name', 'state__name', 'city__name')
    filter_class = filters.LocationFilter
