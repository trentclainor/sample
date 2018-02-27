from django_filters import rest_framework as filters

from sample.common.models import ExternalRole


class ExternalRoleFilter(filters.FilterSet):
    name = filters.CharFilter(name='title', lookup_expr='istartswith')

    class Meta:
        model = ExternalRole
        fields = ('name',)
