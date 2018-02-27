from rest_framework import serializers

from sample.vacancies.models import Message


class MessageSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'job_profile', 'text', 'status', 'created_at')

    def get_parent_pk(self):
        parent_pk = None
        view = self.context.get('view')
        if view and hasattr(view, 'parent_pk'):
            parent_pk = view.parent_pk
        return parent_pk

    def create(self, validated_data):
        validated_data.update({'vacancy_id': self.get_parent_pk()})
        return super(MessageSerializer, self).create(validated_data)
