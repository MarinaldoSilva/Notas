import pytest
from django.contrib.auth import get_user_model

"""
referência o users.User que esta setado no AUTH_USER_MODEL do settings.py"""
User = get_user_model()

"""
decorator do pytest-django que vai indicar que temos que acessar o banco de dados, e assim garante que será criado um BD limpo para os testes, sem isso não é possível testar os processos de criação"""


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        username="test_user", password="admin@2025", email="test@exemple.com"
    )

    assert user.username == "test_user"
    assert user.check_password("admin@2025")
    assert user.email == "test@exemple.com"
    assert user.is_active is True
    assert not user.is_superuser
    assert not user.is_staff


@pytest.mark.django_db
def test_create_superuser():
    sudo = User.objects.create_superuser(
        username="sudosu", password="admin@2025", email="sudosu@exemple.com"
    )

    assert sudo.username == "sudosu"
    assert sudo.email == "sudosu@exemple.com"
    assert sudo.check_password("admin@2025")
    assert sudo.is_staff is True
    assert sudo.is_active is True
    assert sudo.is_superuser is True
