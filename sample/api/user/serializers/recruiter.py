from django.contrib.auth import get_user_model
from rest_framework import serializers

from sample.api.user.serializers import CompanySerializer
from sample.users.models import Company

User = get_user_model()


class RecruiterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'company')

    def create(self, validated_data):
        company = validated_data.pop('company', None)
        user = User.objects.create_recruiter(
            validated_data.get('email'),
            validated_data.get('password'),
            name=validated_data.get('name'),
        )
        Company.objects.update_or_create(user=user, defaults=CompanySerializer(company).data)
        user.save()
        return user
