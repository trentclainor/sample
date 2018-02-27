from django.contrib.auth import get_user_model
from rest_framework import serializers

from sample.job_profiles.models import WorkHistory

User = get_user_model()


class WorkHistorySerializer(serializers.ModelSerializer):
    job_type = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WorkHistory
        fields = ('id', 'role', 'company_name', 'descr', 'job_type', 'start_date', 'end_date', 'experience')

    def get_job_type(self, obj):
        return obj.get_job_type_display()

    def get_experience(self, instance):
        exp = instance.experience
        return {
            'years': exp.years,
            'months': exp.months,
            'days': exp.days,
        }

    def get_parent_pk(self):
        parent_pk = None
        view = self.context.get('view')
        if view and hasattr(view, 'parent_pk'):
            parent_pk = view.parent_pk
        return parent_pk

    def create(self, validated_data):
        validated_data.update({'job_profile_id': self.get_parent_pk()})
        return super(WorkHistorySerializer, self).create(validated_data)
