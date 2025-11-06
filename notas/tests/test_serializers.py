import pytest
from datetime import datetime
from django.contrib.auth import get_user_model
from notas.models import Notas
from notas.serializer import NotasSerializer

User = get_user_model()

"""fixture cria um objeto para ser usado nos testes"""
@pytest.fixture
@pytest.mark.django_db
def user_test():
    return User.objects.user_test(
        username='user_test',
        password='admin@25',
        email='teste@exemple.com'
    )

"""nota que vai servir para testar o processo de update e reader"""
@pytest.fixture
@pytest.mark.django_db
def nota_teste(user_test):
    return Notas.objects.create(
        dono=user_test,
        titulo='teste nota com dono',
        descricao='descrição da nota do user',
        status=1
    )


@pytest.mark.django_db
def nota_serializer_valida(user_test):
    request_data = {
        'titulo':'titulo teste',
        'descricao':'descriçao de teste',
        'status': 1
    }

    serializer = NotasSerializer(data=request_data, context={'request':{'user':user_test}})
    assert serializer.is_valid(raise_exception=True)
    nota = serializer.save(dono=user_test)

    assert nota.titulo == 'titulo de teste' 
    assert nota.descricao == 'descriçao de teste'
    assert nota.status == 1
    assert nota.dono == user_test
    assert nota.objects.count() == 1


@pytest.mark.django_db
def nota_serializer_titulo_curto(user_test):
    request_data = {
        'titulo':'curto',
        'descricao':'descrição valida para a nota',
        'status':1
    }

    serializer = NotasSerializer(data=request_data, context={'request':{'user':user_test}})
    assert not serializer.is_valid(raise_exception=True)
    nota = serializer.save(dono=user_test)

    assert 'titulo' in serializer.errors
    assert 'O titulo deve ter pelo menos 3 palavras' in serializer.errors['titulo'][0]


@pytest.mark.django_db
def nota_serializer_titulo_descricao_igual(user_test):
    request_data = {
        'titulo':'um dois tres',
        'descricao':'um dois tres',
        'status':1
    }

    serializer = NotasSerializer(data=request_data, context={'request':{'user':user_test}})
    assert not serializer.is_valid(raise_exception=True)
    nota = serializer.save(dono=user_test)

    """
    os campos estão corretos, mas a regra de negócio não acusou quebra de protocolo com a igualdade, então deu o non_field_errors no serializer.errors"""
    assert 'non_field_errors' in serializer.errors
    assert 'O titulo não pode ser igual a descrição da nota.' in serializer.errors['non_field_errors'][0]


@pytest.mark.django_db
def atualizar_nota_existente(nota_teste):
    request_data = {
        'titulo':'Novo titulo da nota',
        'descricao':'atualizar descrição da nota',
        'status':3
    }

    serializer = NotasSerializer(instance=nota_teste, data=request_data, partil=True)
    assert serializer.is_valid(raise_exception=True)
    update_nota = serializer.save()

    assert update_nota.titulo == 'Novo titulo da nota'
    assert update_nota.descricao == 'atualizar descrição da nota'
    assert update_nota.status == 3
    assert update_nota.data_criacao == nota_teste.data_criacao
    assert update_nota.refresh_from_db()
    assert nota_teste.titulo == 'Novo titulo da nota'