# Notas API

<p align="center">
<br>
API REST para gerenciamento pessoal de notas, com autenticação de usuário.
</p>

## Sobre o Projeto

O projeto `Notas` foi feito com Django e Django REST Framework, é uma API para gerenciamento de notas pessoais onde os usuários criam, editam, visualizam e excluam suas anotações com foco em privacidade e segurança.
O controle de acesso as notas é feito com tokens únicos gerados para cada usúario, com isso temos segurança para usar as anotações da forma que desejar.

## Funcionalidades

### Authentication

- **SignupView :** Rota de cadastro do usuário no sistema, aqui será feito o vinculo do usuário com o Token, e o email, senha e tokens vão ser retornados.
- **SigninView :** Utiliza o email e senha no body para validação e na segurança passados o token vinculado ao usuário.
- **SignoutView:** Recebe o token do usuário e o invalida no sistema

### Usuários

- **Listagem de usuários:** Listagem de usuário onde é exibido as informações do User
- **Edição de usuários:** Cada usuário pode alterar seu nome, email, foto de perfil e primeiro e segundo nome.

### Notas

- **Criação de Notas:** Usuários autenticados podem criar novas notas, e a cada criação de nota é disparado um E-mail informando ao usuário.
- **Listagem de Notas:** Os usuários logados podem ver suas anotações.
- **Atualização de Notas:** É possível editar um titulo e descrição da nota, e quando isso é feito um selo com a data da atualização é adicionado.
- **Excluir Notas:** Apagar notas existentes.
- **Requisitos de criação de notas:**
  - Título: mínimo de 3 palavras.
  - Titulo e descrição: Não podem ser iguais

## Tecnologias

- **Django**
- **Django REST Framework**
- **Python**
- **SQLite3**

## Executar

### 1. Baixar o repositório de notas

```bash
git clone https://github.com/marinaldosilva/notas.git
```

### 2. Criar um ambiente virtual venv

```bash
python -m venv venv
venv/bin/activate
```

### 3. Instalar libs do projeto

Instale o arquivo `requirements.txt` para instalar todas as libs.

```bash
pip install -r requirements.txt
```

### 4. Instância do banco de dados

Utilizamos o banco padrão que se chama sqlite3.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar um Superusuário

para acessar o Django admin para gerenciar os usuários e notas, crie um superuser:

```bash
python manage.py createsuperuser
```

### 6. Executar o projeto

```bash
python manage.py runserver
```

O endereço será `http://127.0.0.1:8000/` é padrão do Django.

## Endpoints

### Autenticação

#### Criação de usuário com Token

- Rota: `/api/v1/user/auth/register/`

Todos os dados são obrigatórios no registro.

```json
{
  "username": "cehole",
  "email": "cehole1694@agenra.com",
  "first_name": "cehole",
  "last_name": "cehole",
  "password": "admin@25"
}
```

Entrar no sistema após o cadastro.

- Rota: `/api/v1/user/auth/login/`

```http
http://127.0.0.1:8000//api/v1/user/auth/login/
```

```json
{
  "email": "cehole1694@agenra.com",
  "password": "admin@25"
}
```

Quando a rota de login é acessada com o email e senha, se forem validos, os tokens serão retornados

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyOTYyMDI1LCJpYXQiOjE3NjI5NTg0MjUsImp0aSI6ImU3YWNkMjI2MDJmMDQyYjBhNWYxOWE3ZWUxZTM1NDA1IiwidXNlcl9pZCI6IjkifQ.7-u-fhn_rRnzev0xFsbkDATodkOkE1uY42FCkOuebN8",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MzY0OTYyNSwiaWF0IjoxNzYyOTU4NDI1LCJqdGkiOiIzMjljZGU5MjQxZWM0MzQ4ODdjZDFjNTc4OTdmMzYyOCIsInVzZXJfaWQiOiI5In0.D4-2rpduwvyTm5SMzkutPr9xhP4zo5UDHIih2ZXPwaM"
}
```

Sair do sistema e invalidando o token.

- Rota: `http://127.0.0.1:8000/api/v1/auth/logout/`

Passamos o token refresh para o sistema invalidar.

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MjYyNjcwNSwiaWF0IjoxNzYxOTM1NTA1LCJqdGkiOiJjMWE5ZTNiZWYyYjc0ZGFiOWMyNjM2ZTc0NjU0NTI1NyIsInVzZXJfaWQiOiI1In0.b5tbGAt60s8XQcmGwMV9fJiRbqtIrHgnuZdoXKkjjr8"
}
```

### Notas

#### Listagem de Notas do usuário que as criou.

- Rota: `/api/v1/notas/listar/`

```http
http://127.0.0.1:8000//api/v1/notas/meu_perfil/
```

```json
{
  "id": 1,
  "username": "kiko",
  "first_name": "kiko",
  "last_name": "jin",
  "avatar": "/media/avatars/default.png",
  "email": "kikojin961@agenra.com"
}
```

#### Criar Nova Nota

- Rota: `/api/v1/notas/criar/`

```http
http://127.0.0.1:8000/api/v1/notas/criar/
```

```json
{
  "titulo": "Comprar Pão E Leite",
  "descricao": "Passar no mercado antes de voltar pra casa."
}
```

```json
{
  "result": {
    "id": 3,
    "titulo": "Comprar Pão E Leite",
    "descricao": "Passar no mercado antes de voltar pra casa."
  }
}
```

#### Detalhes de uma Nota Específica

- URL: `/api/v1/notas/listar/<int:pk>/`

```http
POST http://127.0.0.1:8000/api/v1/notas/listar/
```

Retorna uma nota especifica de acordo com o ID passado na requisição.

```json
{
    {
	"id": 1,
	"dono": "Armani42",
	"titulo": "Product Security Supervisor",
	"descricao": null,
	"data_criacao": "2025-10-29T19:35:37.468916Z",
	"status": 1
	}
}
```

#### Atualizar uma Nota Específica

- Rota:`/api/v1/notas/editar/<int:id>/`

```http
http://127.0.0.1:8000/api/v1/notas/editar/2/

{
    {
	"titulo":"Robson de valerio",
	"descricao":"amigo colorido de valerio",
	"status": 1
    }
}
```

#### Deletar uma Nota Específica

- URL: `/notas/<int:pk>/`

```http
http://127.0.0.1:8000/api/v1/notas/deletar/3/
```

Retorno: 240 no content

### Teste básicos de software

Os testes das views e serializres de `Notas` foram criados para garantir que o sistema tenha o comportamento correto, para isso temos os testes básicos de software:

Criando user autenticado

```py
@pytest.fixture
@pytest.mark.django_db
def usuário_autenticado(api_client):
    user=User.objects.create_user(
        username='teste',
        password='admin@25',
        email='teste@gmail.com'
    )
    api_client.force_authenticate(user)
    return user
```

Retornando um user autenticado para testar a criação de notas.

Craindo um nota com o user autenticado.

```py
@pytest.mark.django_db
def test_notas_list_autenticado_com_notas(usuário_autenticado, api_client):
    mixer.cycle(3).blend(Notas, dono=usuário_autenticado, titulo=mixer.FAKE, descricao=mixer.FAKE)
    url = reverse('listar_nota')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()['result']) == 3
```

Criando um user não autenticado

```py
@pytest.fixture
@pytest.mark.django_db
def usuario_nao_autenticado(api_client):
    api_client.force_authenticate(user=None)
    return None
```

Criando uma anotação com user não autenticado

```py
@pytest.mark.django_db
def test_usuario_nao_autenticado_criar_notas(api_client):
    url = reverse('criar_nota')
    request_data = {'titulo':'Novo Titu Agora', 'descricao':'Tes Desc Novo'}
    response = api_client.post(url, request_data, format='json')
    assert response.status_code == 401
```

Esses são os testes básicos, existem outros no que estão na pasta tests de cada App(Notas e User até o momento).
