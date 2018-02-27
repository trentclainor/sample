from django.contrib.auth import get_user_model
from rest_framework import serializers

from sample.api.serializers import ArrayMultipleChoiceField
from sample.common.models import JOB_TYPES
from sample.job_profiles.models import Preferences

User = get_user_model()


class PreferencesSerializer(serializers.ModelSerializer):
    looking_for = ArrayMultipleChoiceField(choices=JOB_TYPES, required=False)

    class Meta:
        model = Preferences
        fields = ('id', 'industries', 'roles', 'location', 'looking_for')

    def get_parent_pk(self):
        parent_pk = None
        view = self.context.get('view')
        if view and hasattr(view, 'parent_pk'):
            parent_pk = view.parent_pk
        return parent_pk

    def create(self, validated_data):
        validated_data.update({'job_profile_id': self.get_parent_pk()})
        return super(PreferencesSerializer, self).create(validated_data)
