from django_filters import rest_framework as filters

from sample.common.models import Role


class RoleFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Role
        fields = ('id', 'name',)
