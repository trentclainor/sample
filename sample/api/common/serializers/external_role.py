from rest_framework import serializers

from sample.common.models import ExternalRole


class ExternalRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='title_id')
    name = serializers.CharField(source='title')

    class Meta:
        model = ExternalRole
        fields = ('id', 'name')
