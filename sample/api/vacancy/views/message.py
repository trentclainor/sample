from django.contrib.auth import get_user_model

from sample.api.base_viewset import NestedModelViewSet
from sample.api.vacancy import serializers
from sample.vacancies.models import Message, Vacancy

User = get_user_model()


class MessageViewSet(NestedModelViewSet):
    serializer_class = serializers.MessageSerializer
    parent_lookup = 'vacancy'

    def get_parent_queryset(self):
        if self.request.user and self.request.user.is_authenticated and self.request.user.is_recruiter:
            return Vacancy.objects.filter(company__user=self.request.user)
        return Vacancy.objects.none()

    def get_queryset(self):
        if self.is_valid_parent_pk():
            return Message.objects.filter(vacancy_id=self.parent_pk)
        return Message.objects.none()
