from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notas.utils import ERROR_PERMISSION_DENIED, KEY_ERROR, USER_LOCALIZATION

from .models import User
from .serializer import UserSerializer


class UserListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        """
        Quando o serializer é chamado em sem passar o data=, é chamado em modo leitura(get), e passamos o primeiro argumento que é instance, ele recebe o request.user que já é um objeto completo com id, username, email e etc... e tras esses dados que serão serializados que são um dict e o Response os converte em JSON
        """
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            queryset = User.objects.get(pk=pk)
            if request.user.id != queryset.id and not request.user.is_staff and not request.user.is_superuser:
                return Response(
                    {KEY_ERROR: ERROR_PERMISSION_DENIED},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except User.DoesNotExist:
            return Response({KEY_ERROR: USER_LOCALIZATION}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
