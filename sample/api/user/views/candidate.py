from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sample.api.user import serializers

User = get_user_model()


class CandidateRegisterView(CreateAPIView):
    """View for register candidate user"""
    serializer_class = serializers.CandidateSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = serializer.data
        response['token'] = serializer.instance.auth_token.key
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
