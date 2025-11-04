from django.urls import path
from .views import (NotasListAPIView, NotasDetailAPIView, NotasCreateAPIView, NotasUpdateAPIView, NotasDestroyAPIView)

urlpatterns = [

    path('criar/', NotasCreateAPIView.as_view(), name='criar_nota'),
    path('listar/', NotasListAPIView.as_view(), name='listar_nota'),
    path('listar/<int:pk>/', NotasDetailAPIView.as_view(), name='listar_nota_pk'),
    path('editar/<int:pk>/', NotasUpdateAPIView.as_view(), name='update_nota'),
    path('deletar/<int:pk>/', NotasDestroyAPIView.as_view(), name='deletar_nota')
    
]