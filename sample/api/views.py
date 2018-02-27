from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken as RestObtainAuthToken

from sample.api.authentication_classes import CsrfExemptSessionAuthentication
from sample.api.user.serializers.user import UserSerializer


class ObtainAuthToken(RestObtainAuthToken):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user)
        return Response({'token': token.key, 'user': user_data.data})
