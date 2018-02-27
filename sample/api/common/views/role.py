from rest_framework.viewsets import ModelViewSet

from sample.api.common import filters, serializers
from sample.common.models import Role


class RoleViewSet(ModelViewSet):
    """
    ViewSet for listing roles
    """

    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer
    search_fields = ('name',)
    filter_class = filters.RoleFilter
