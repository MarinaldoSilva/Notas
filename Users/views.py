from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework import status
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated

class UserListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        try:
            queryset = User.objects.get(pk=pk)
            if request.user.id != queryset.id:
                return Response({"errors":"você não term permissão para alterar esse usuário"})
        except User.DoesNotExist:
            return Response({"error":"Usuário não localizado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    