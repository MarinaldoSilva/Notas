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
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            queryset = User.objects.get(pk=pk)
            if (
                request.user.id != queryset.id
                and not request.user.is_staff
                and not request.user.is_superuser
            ):
                return Response(
                    {KEY_ERROR: ERROR_PERMISSION_DENIED},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except User.DoesNotExist:
            return Response(
                {KEY_ERROR: USER_LOCALIZATION}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
