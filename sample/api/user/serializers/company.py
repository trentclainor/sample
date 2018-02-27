from rest_framework import serializers

from sample.users.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'logo', 'name', 'website', 'address', 'descr')

    def get_parent_pk(self):
        parent_pk = None
        view = self.context.get('view')
        if view and hasattr(view, 'parent_pk'):
            parent_pk = view.parent_pk
        return parent_pk

    def create(self, validated_data):
        validated_data.update({'user_id': self.get_parent_pk()})
        return super(CompanySerializer, self).create(validated_data)
