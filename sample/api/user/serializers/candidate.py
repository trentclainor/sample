from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CandidateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name')

    def create(self, validated_data):
        user = User.objects.create_candidate(
            validated_data.get('email'),
            validated_data.get('password'),
            name=validated_data.get('name'),
        )
        user.save()
        return user
