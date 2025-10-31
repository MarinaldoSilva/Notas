from django.urls import path
from .views import SignupView, SigninView, SignoutView

urlpatterns = [
    path('register/', SignupView.as_view(), name='criar_user'),
    path('login/', SigninView.as_view(), name='login_user'),
    path('logout/', SignoutView.as_view(), name='logout_user'),
]