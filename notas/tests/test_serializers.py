import pytest
from django.contrib.auth import get_user_model

from notas.models import Notas
from notas.serializer import NotasSerializer

User = get_user_model()

"""fixture cria um objeto para ser usado nos testes"""


@pytest.fixture
@pytest.mark.django_db
def user_teste():
    return User.objects.create_user(
        username="user_teste", password="admin@25", email="teste@exemple.com"
    )


"""nota que vai servir para testar o processo de update e reader"""


@pytest.fixture
@pytest.mark.django_db
def nota_teste(user_teste):
    return Notas.objects.create(
        dono=user_teste, titulo="teste nota com dono", descricao="descrição da nota do user", status=1
    )


@pytest.mark.django_db
def test_nota_serializer_valida(user_teste):
    request_data = {"titulo": "Titulo Teste Teste", "descricao": "descriçao de teste", "status": 1}

    serializer = NotasSerializer(data=request_data, context={"request": {"user": user_teste}})
    assert serializer.is_valid(raise_exception=True)
    nota = serializer.save(dono=user_teste)

    assert nota.titulo == "Titulo Teste Teste"
    assert nota.descricao == "descriçao de teste"
    assert nota.status == 1
    assert nota.dono == user_teste
    assert Notas.objects.count() == 1


@pytest.mark.django_db
def test_nota_serializer_titulo_curto(user_teste):
    request_data = {"titulo": "curto", "descricao": "descrição valida para a nota", "status": 1}

    serializer = NotasSerializer(data=request_data, context={"request": {"user": user_teste}})
    assert not serializer.is_valid()
    assert "titulo" in serializer.errors


@pytest.mark.django_db
def test_nota_serializer_titulo_descricao_igual(user_teste):
    request_data = {"titulo": "um dois tres", "descricao": "um dois tres", "status": 1}

    serializer = NotasSerializer(data=request_data, context={"request": {"user": user_teste}})
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_atualizar_nota_existente(nota_teste):
    request_data = {
        "titulo": "novo titulo da nota",
        "descricao": "atualizar descrição da nota",
        "status": 3,
    }

    serializer = NotasSerializer(instance=nota_teste, data=request_data, partial=True)
    assert serializer.is_valid()
    update_nota = serializer.save()

    assert update_nota.titulo == "Novo Titulo Da Nota"
    assert update_nota.descricao == "atualizar descrição da nota"
    assert update_nota.status == 3
    # assert update_nota.refresh_from_db()
