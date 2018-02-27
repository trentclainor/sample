from django_filters import rest_framework as filters

from sample.common.models import City, Country, Location, State


class LocationFilter(filters.FilterSet):
    country_name = filters.CharFilter(name='country__name', lookup_expr='istartswith')
    state_name = filters.CharFilter(name='state__name', lookup_expr='istartswith')
    city_name = filters.CharFilter(name='city__name', lookup_expr='istartswith')
    country_id = filters.ModelMultipleChoiceFilter(queryset=Country.objects.all(), lookup_expr='in')
    state_id = filters.ModelMultipleChoiceFilter(queryset=State.objects.all(), lookup_expr='in')
    city_id = filters.ModelMultipleChoiceFilter(queryset=City.objects.all(), lookup_expr='in')

    class Meta:
        model = Location
        fields = ('country_id', 'country_name', 'state_id', 'state_name', 'city_id', 'city_name',)
