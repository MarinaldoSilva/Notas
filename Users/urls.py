from django.urls import path
from .views import UserListAPIView, UserUpdateAPIView

urlpatterns = [
    path("listar/", UserListAPIView.as_view(), name='user_list'),
    path("editar/", UserUpdateAPIView.as_view(), name='editar_user')
]
