from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notas
from .serializer import NotasSerializer


class NotasListAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Notas.objects.filter(dono=request.user)
        serializer = NotasSerializer(queryset, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

class NotasDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            queryset = Notas.objects.get(pk=pk, dono=request.user)
            serializer = NotasSerializer(queryset)
        except Notas.DoesNotExist:
            return Response({"error":serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)
    
class NotasCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = NotasSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(dono=request.user)
        except Notas.DoesNotExist:
            return Response({"error":serializer.errors}, status=status.HTTP_404)
        return Response({"result":serializer.data}, status=status.HTTP_201_CREATED)

class NotasUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            queryset = Notas.objects.get(pk=pk, dono=request.user)
        except Notas.DoesNotExist:
            return Response({"error":"Anotação não localizada"})
        serializer = NotasSerializer(instance=queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(dono=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotasDestroyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            queryset = Notas.objects.get(pk=pk, dono=request.user)
            queryset.delete()
        except Notas.DoesNotExist:
            return Response({"error":"Anotação não localizada"})
        return Response(status=status.HTTP_204_NO_CONTENT)
 
