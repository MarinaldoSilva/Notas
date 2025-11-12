from django.urls import path

from .views import UserListAPIView, UserUpdateAPIView

urlpatterns = [
    path("meu_perfil/", UserListAPIView.as_view(), name="user_list"),
    path("editar/<int:pk>/", UserUpdateAPIView.as_view(), name="editar_user_id"),
]
