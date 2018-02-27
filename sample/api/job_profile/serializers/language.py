from django.contrib.auth import get_user_model
from rest_framework import serializers

from sample.job_profiles.models import Language

User = get_user_model()


class LanguageSerializer(serializers.ModelSerializer):
    level_display = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = ('id', 'name', 'level_display', 'level')

    def get_level_display(self, obj):
        return obj.get_level_display()

    def get_parent_pk(self):
        parent_pk = None
        view = self.context.get('view')
        if view and hasattr(view, 'parent_pk'):
            parent_pk = view.parent_pk
        return parent_pk

    def create(self, validated_data):
        validated_data.update({'job_profile_id': self.get_parent_pk()})
        return super(LanguageSerializer, self).create(validated_data)
