from django_filters import rest_framework as filters

from sample.common.models import Country


class CountryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Country
        fields = ('id', 'name',)
