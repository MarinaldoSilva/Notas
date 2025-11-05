# Auth/views.py
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.models import User
from users.serializer import UserSerializer


class SignupView(APIView):

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh_token = TokenObtainPairSerializer.get_token(user)
        access_token = refresh_token.access_token

        return Response(
            {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "access": str(access_token),
                "refresh": str(refresh_token),
            },
            status=status.HTTP_201_CREATED,
        )


class SigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Email não localizado."}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            refresh_token = TokenObtainPairSerializer.get_token(user)
            access_token = refresh_token.access_token

            return Response(
                {"access": str(access_token), "refresh": str(refresh_token)},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Credenciais inválidas.."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        refresh_token = request.data.get("refresh")
        user = request.user
        if not refresh_token:
            return Response(
                {"error": "Token para atualização não foi enviado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            user.save()
            token.blacklist()
        except TokenError:
            raise AuthenticationFailed("Erro ao invalidar o token.", code=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_205_RESET_CONTENT)
