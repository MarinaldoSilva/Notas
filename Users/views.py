from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
#from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class UserCreateAPIView(APIView):
    """
        Cria um usuário e retorna o token(jwt) com o access token e refresh token
    """
    
    permission_classes = [AllowAny]

    @extend_schema(
            summary="Cadstro de usuário já com o token",
            request=UserSerializer,
            responses={
                201: OpenApiExample(
                    'Resposta da requisição',
                    value={
                        'user_id':'1',
                        'username': 'name_user',
                        'email': 'email_address',
                        'access': 'jkfbhsjkefbkjesfh',
                        'refresh': 'kgjlsdrgjldrkjgg'
                    }
                )
            }
    )
    def post(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = TokenObtainPairSerializer.get_token(user)
        access_token = refresh_token.access_token
        return Response({
            'user_id':user.id,
            'username': user.username,
            'email': user.email,
            'access': str(access_token),
            'refresh': str(refresh_token)
            }, status=status.HTTP_201_CREATED)
