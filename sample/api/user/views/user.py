from django.contrib.auth import get_user_model
from rest_framework.decorators import list_route, detail_route
from rest_framework.viewsets import ReadOnlyModelViewSet

from sample.api.user import serializers

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing or retrieving users
    """
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        if self.request.user:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    @list_route(methods=['get'])
    def me(self, request):
        """
            Returns current user instance.
        """
        self.kwargs['pk'] = request.user.id
        return self.retrieve(request)

    @list_route(methods=['get'])
    def company(self, request):
        """
            Returns current user instance.
        """
        self.kwargs['pk'] = request.user.id
        return self.retrieve(request)
