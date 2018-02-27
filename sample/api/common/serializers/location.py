from rest_framework import serializers

from sample.common.models import Location


class LocationSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    state = serializers.StringRelatedField()
    city = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ('id', 'name', 'country_id', 'country', 'state_id', 'state', 'city_id', 'city')
