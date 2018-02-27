from rest_framework import serializers

from sample.common.models import ExternalSkill


class ExternalSkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='skill_id')
    name = serializers.CharField(source='skill')

    class Meta:
        model = ExternalSkill
        fields = ('id', 'name')
