import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from notas.models import Notas
from mixer.backend.django import mixer
from django.urls import reverse

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def api_client():
    return APIClient()

@pytest.fixture
@pytest.mark.django_db
def usuário_autenticado(api_client):
    user=User.objects.create_user(
        username='teste',
        password='admin@25',
        email='mario@gmail.com'
    )
    api_client.force_authenticate(user)
    """
    as rotas exigem autenticação para acesso, temos que força isso para simular os testes
    com esse metodo ele não gera os tokens, mas força o acesso
    """
    return user

@pytest.fixture
@pytest.mark.django_db
def usuario_nao_autenticado(api_client):
    api_client.force_authenticate(user=None)
    return None


@pytest.mark.django_db
def test_notas_list_nao_autenticado(api_client):
    url = reverse('listar_nota')
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_usuario_autenticado_sem_notas_cadastradas(api_client, usuário_autenticado):
    url = reverse('listar_nota')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {"result":[]}

@pytest.mark.django_db
def test_notas_list_autenticado_com_notas(usuário_autenticado, api_client):
    mixer.cycle(3).blend(Notas, dono=usuário_autenticado, titulo=mixer.FAKE, descricao=mixer.FAKE)
    url = reverse('listar_nota')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()['result']) == 3


@pytest.mark.django_db
def test_usuario_nao_autenticado_criar_notas(api_client):
    url = reverse('criar_nota')
    request_data = {'titulo':'Novo Titu Agora', 'descricao':'Tes Desc Novo'}
    response = api_client.post(url, request_data, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_criar_notas_usuario_autenticado(api_client, usuário_autenticado, mocker):
    mocker.patch('notas.utils.form_email')
    url = reverse('criar_nota')
    data = {
        'titulo':'Nota Nova Teste',
        'descricao': 'ters hsdt ldada'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Notas.objects.count() == 1
    assert Notas.objects.first().titulo == 'Nota Nova Teste'