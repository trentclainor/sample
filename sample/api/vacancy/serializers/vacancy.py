from rest_framework import serializers

from sample.api.serializers import ArrayMultipleChoiceField
from sample.common.models import JOB_TYPES
from sample.vacancies.models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    company = serializers.CharField(read_only=True, default=None)
    types = ArrayMultipleChoiceField(choices=JOB_TYPES, required=False)
    matches = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Vacancy
        fields = ('id', 'name', 'company', 'location', 'industry', 'role', 'types', 'experience_from', 'experience_to',
                  'salary_from', 'salary_to', 'descr', 'modified', 'user', 'matches')

    def create(self, validated_data):
        user = validated_data.pop('user')
        validated_data.pop('company')
        validated_data.pop('matches')
        if user.company:
            validated_data.update({'company': user.company})
        return super(VacancySerializer, self).create(validated_data)
