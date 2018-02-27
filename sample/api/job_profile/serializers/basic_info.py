from django.contrib.auth import get_user_model
from rest_framework import serializers

from sample.job_profiles.models import BasicInfo

User = get_user_model()


class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = ('id', 'photo', 'name', 'email', 'phone', 'linkedin', 'address1', 'address2', 'address3')

    def get_parent_pk(self):
        parent_pk = None
        view = self.context.get('view')
        if view and hasattr(view, 'parent_pk'):
            parent_pk = view.parent_pk
        return parent_pk

    def create(self, validated_data):
        validated_data.update({'job_profile_id': self.get_parent_pk()})
        return super(BasicInfoSerializer, self).create(validated_data)
