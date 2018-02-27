from django.contrib.auth import get_user_model
from rest_framework import serializers

from sample.job_profiles.models import JobProfile

User = get_user_model()


class JobProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    experience = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JobProfile
        fields = ('id', 'name', 'cv', 'is_published', 'is_default', 'user', 'experience')

    def get_experience(self, instance):
        exp = instance.experience
        return {
            'years': exp.years,
            'months': exp.months,
            'days': exp.days,
        }
