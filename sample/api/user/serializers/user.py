from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import CompanySerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'company', 'is_candidate', 'is_recruiter')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
