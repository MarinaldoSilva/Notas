from django.urls import path

from .views import (
    NotasCreateAPIView,
    NotasDestroyAPIView,
    NotasDetailAPIView,
    NotasListAPIView,
    NotasUpdateAPIView,
)

urlpatterns = [
    path("criar/", NotasCreateAPIView.as_view(), name="criar_nota"),
    path("listar/", NotasListAPIView.as_view(), name="listar_nota"),
    path("listar/<int:pk>/", NotasDetailAPIView.as_view(), name="listar_nota_pk"),
    path("editar/<int:pk>/", NotasUpdateAPIView.as_view(), name="editar_nota"),
    path("deletar/<int:pk>/", NotasDestroyAPIView.as_view(), name="apagar_nota"),
]
