from rest_framework import serializers

from sample.vacancies.models import Vacancy


class SearchVacancyPersonalizedSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    location = serializers.StringRelatedField(read_only=True)
    industry = serializers.StringRelatedField(read_only=True)
    role = serializers.StringRelatedField(read_only=True)
    types = serializers.ListField(read_only=True, source='get_types_display')
    score = serializers.DecimalField(max_digits=15, decimal_places=6, read_only=True, default=0.00)

    class Meta:
        model = Vacancy
        fields = ('id', 'name', 'company', 'location', 'industry', 'role', 'types', 'experience_from', 'experience_to',
                  'salary_from', 'salary_to', 'descr', 'modified', 'score')
