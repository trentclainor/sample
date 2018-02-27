from django_filters import rest_framework as filters

from sample.common.models import Industry


class IndustryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Industry
        fields = ('id', 'name',)
