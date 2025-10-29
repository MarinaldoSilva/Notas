from django.urls import path
from .views import UserCreateAPIView

urlpatterns = [
    path("user/cadastro/", UserCreateAPIView.as_view(), name='user_create')
]