from rest_framework.viewsets import ModelViewSet

from sample.api.common import filters, serializers
from sample.common.models import ExternalSkill


class ExternalSkillViewSet(ModelViewSet):
    """
    ViewSet for listing external skills
    """

    queryset = ExternalSkill.objects.all()
    serializer_class = serializers.ExternalSkillSerializer
    search_fields = ('skill',)
    filter_class = filters.ExternalSkillFilter
