from django.contrib.auth import get_user_model
from rest_framework import serializers

from sample.job_profiles.models import Education

User = get_user_model()


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('id', 'school', 'degree', 'start_date', 'end_date')

    def get_parent_pk(self):
        parent_pk = None
        view = self.context.get('view')
        if view and hasattr(view, 'parent_pk'):
            parent_pk = view.parent_pk
        return parent_pk

    def create(self, validated_data):
        validated_data.update({'job_profile_id': self.get_parent_pk()})
        return super(EducationSerializer, self).create(validated_data)
