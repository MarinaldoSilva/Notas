from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notas
from .utils import form_email
from .serializer import NotasSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

class NotasListAPIView(APIView):
    """
        Listagem de notações já cadastradas de usuários autenticados.
    """
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Listagem de notações",
            responses={200:NotasSerializer(many=True)},
            examples=[
                OpenApiExample(
                    'Demonstrativo de listagem',
                    value={
                        'result':[
                            {"id": 1, "dono": "user", "titulo": "titulo da nota", "descricao": "descrição da primeira nota.", "data_criacao": "2025-10-31T10:00:00Z", "status": 3},
                        {"id": 2, "dono": "user2", "titulo": "titulo da nota 2", "descricao": "descrição da segunda nota.", "data_criacao": "2025-10-31T11:00:00Z", "status": 2},
                        ]
                    }
                )
            ]

    )
    def get(self, request):
        queryset = Notas.objects.filter(dono=request.user)
        serializer = NotasSerializer(queryset, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

class NotasDetailAPIView(APIView):
    """
        Mostra um nota em especifico recuperada pelo PK/ID
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="Listar nota especifica",
            responses={200:NotasSerializer, 404:{'error':'nota não localizada'}},
            parameters=[
                OpenApiParameter(name='pk', type=int,location=OpenApiParameter.PATH, description='ID da nota.')
            ],
            examples=[
                OpenApiExample(
                    'Demonstração de listagem por ID',
                    value={
                        'result':
                            {"id": 1, "dono": "user", "titulo": "titulo da nota", "descricao": "descrição da primeira nota.", "data_criacao":"2025-10-31T10:00:00Z", "status": 3},
                    }
                )
            ]


    )
    def get(self, request, pk):
        try:
            queryset = Notas.objects.get(pk=pk, dono=request.user)
            serializer = NotasSerializer(queryset)
        except Notas.DoesNotExist:
            return Response({"error":serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)
    
class NotasCreateAPIView(APIView):
    """
        Criação de anotações para usuários autenticados
    """
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Cria uma nova notação",
        request=NotasSerializer,
        responses={
            201: NotasSerializer,
            400: {'error': 'dados invalidos'}
        }
    )
    
    def post(self, request):
        try:
            serializer = NotasSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            notas_instance = serializer.save(dono=request.user)
            user_email = request.user.email
            titulo_nota = notas_instance.titulo
            form_email(user_email, titulo_nota)
            print(f"E-mail de criação de nota enviado para {user_email} com título '{titulo_nota}'.")
        except Notas.DoesNotExist:
            return Response({"error":serializer.errors}, status=status.HTTP_404)
        return Response({"result":serializer.data}, status=status.HTTP_201_CREATED)

class NotasUpdateAPIView(APIView):
    """
        Editar os valores de titulo e descrição da anotação
    """
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Atualiza uma nota existente de usuário autenticado",
        request=NotasSerializer(),
        responses={
            200: NotasSerializer,
            400: {'error': 'dados invalidos.'},
            404: {'error': 'notação não localizada para esse usuário.'}
        },
        parameters=[
            OpenApiParameter(name='pk', type=int, 
                             description='ID da nota a ser atualizada.'),
        ],
    )
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
    """
        Apagar anotação de usuários autenticados que são donos da nota
    """
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Apagar anotação",
        responses={
            204: {'error': 'excluido com exito.'},
            404: {'error': 'notação não localizada para esse usuário.'}
        },
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH,
                             description='ID da nota a ser apagada.'),
        ],
    )
    def delete(self, request, pk):
        try:
            queryset = Notas.objects.get(pk=pk, dono=request.user)
            queryset.delete()
        except Notas.DoesNotExist:
            return Response({"error":"Anotação não localizada"})
        return Response(status=status.HTTP_204_NO_CONTENT)
 
