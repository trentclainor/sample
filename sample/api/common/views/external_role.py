from rest_framework.viewsets import ModelViewSet

from sample.api.common import filters, serializers
from sample.common.models import ExternalRole


class ExternalRoleViewSet(ModelViewSet):
    """
    ViewSet for listing external roles
    """

    queryset = ExternalRole.objects.all()
    serializer_class = serializers.ExternalRoleSerializer
    search_fields = ('skill',)
    filter_class = filters.ExternalRoleFilter
