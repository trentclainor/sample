from django_filters import rest_framework as filters

from sample.api.filters import ArrayFilter
from sample.common.models import City, Country, Industry, JOB_TYPES, Role, State
from sample.vacancies.models import Vacancy


class FilterSearchVacancyStandard(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    country_id = filters.ModelMultipleChoiceFilter(name='location__country_id', queryset=Country.objects.all(),
                                                   lookup_expr='in')
    state_id = filters.ModelMultipleChoiceFilter(name='location__state_id', queryset=State.objects.all(),
                                                 lookup_expr='in')
    city_id = filters.ModelMultipleChoiceFilter(name='location__city_id', queryset=City.objects.all(),
                                                lookup_expr='in')
    industry = filters.CharFilter(name='industry__name', lookup_expr='icontains')
    industry_id = filters.ModelMultipleChoiceFilter(queryset=Industry.objects.all(), lookup_expr='in')
    role = filters.CharFilter(name='role__name', lookup_expr='icontains')
    role_id = filters.ModelMultipleChoiceFilter(queryset=Role.objects.all(), lookup_expr='in')
    types = ArrayFilter(choices=JOB_TYPES, lookup_expr='overlap')

    class Meta:
        model = Vacancy
        fields = ['name']
