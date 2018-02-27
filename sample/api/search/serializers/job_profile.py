from rest_framework import serializers

from sample.api.job_profile.serializers import BasicInfoSerializer
from sample.job_profiles.models import JobProfile, Preferences


class PreferencesSerializer(serializers.ModelSerializer):
    looking_for = serializers.ListField(read_only=True, source='get_looking_for_display')
    industries = serializers.StringRelatedField(many=True, read_only=True)
    roles = serializers.StringRelatedField(many=True, read_only=True)
    location = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Preferences
        fields = ('id', 'industries', 'roles', 'location', 'looking_for',)


class SearchJobProfileSerializer(serializers.ModelSerializer):
    basic_info = BasicInfoSerializer(read_only=True)
    score = serializers.DecimalField(max_digits=15, decimal_places=6, read_only=True, default=0.0)
    experience = serializers.SerializerMethodField(read_only=True)
    preferences = PreferencesSerializer()

    class Meta:
        model = JobProfile
        fields = ('id', 'name', 'experience', 'basic_info', 'preferences', 'score')

    def get_experience(self, instance):
        exp = instance.experience
        return {
            'years': exp.years,
            'months': exp.months,
            'days': exp.days,
        }
