from django.urls import path
from .views import (NotasListAPIView, NotasDetailAPIView, 
                    NotasCreateAPIView, NotasUpdateAPIView, NotasDestroyAPIView)

urlpatterns = [
    path('notas/listar/', NotasListAPIView.as_view(), name='listar_nota'),
    path('notas/listar/<int:pk>/', NotasDetailAPIView.as_view(), name='listar_nota_pk'),
    path('notas/criar/', NotasCreateAPIView.as_view(), name='criar_nota'),
    path('notas/editar/<int:pk>/', NotasUpdateAPIView.as_view(), name='update_nota'),
    path('notas/deletar/<int:pk>/', NotasDestroyAPIView.as_view(), name='deletar_nota')
]