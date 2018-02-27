from django_filters import rest_framework as filters

from sample.api.filters import ArrayFilter
from sample.common.models import City, Country, Industry, JOB_TYPES, Role, State
from sample.job_profiles.models import JobProfile


class FilterSearchJobProfile(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    country_id = filters.ModelMultipleChoiceFilter(name='preferences__location__country_id',
                                                   queryset=Country.objects.all(), lookup_expr='in')
    state_id = filters.ModelMultipleChoiceFilter(name='preferences__location__state_id', queryset=State.objects.all(),
                                                 lookup_expr='in')
    city_id = filters.ModelMultipleChoiceFilter(name='preferences__location__city_id', queryset=City.objects.all(),
                                                lookup_expr='in')
    industry = filters.CharFilter(name='preferences__industries__name', lookup_expr='icontains')
    industries = filters.ModelMultipleChoiceFilter(name='preferences__industries', queryset=Industry.objects.all(),
                                                   lookup_expr='in')
    role = filters.CharFilter(name='preferences__roles__name', lookup_expr='icontains')
    role_id = filters.ModelMultipleChoiceFilter(name='preferences__roles', queryset=Role.objects.all(),
                                                lookup_expr='in')
    types = ArrayFilter(name='preferences__looking_for', choices=JOB_TYPES, lookup_expr='overlap')

    class Meta:
        model = JobProfile
        fields = ['name']
