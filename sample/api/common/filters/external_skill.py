from django_filters import rest_framework as filters

from sample.common.models import ExternalSkill


class ExternalSkillFilter(filters.FilterSet):
    name = filters.CharFilter(name='skill', lookup_expr='istartswith')

    class Meta:
        model = ExternalSkill
        fields = ('name',)
