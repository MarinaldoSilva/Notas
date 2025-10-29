from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class UserCreateAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, criar = Token.objects.get_or_create(user=user)
        return Response({
            'user_id':user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
            }, status=status.HTTP_201_CREATED)
