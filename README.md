# Notas API

<p align="center">
<br>
API REST para gerenciamento pessoal de notas, com autenticação de usuário.
</p>

<p align="center">
  <a href="#sobre-o-projeto">Projeto</a> -
  <a href="#funcionalidades">Funcionalidades</a> -
  <a href="#tecnologias">Tecnologias</a> -
  <a href="#executar">Testar o projeto em sua máquina</a> -
  <a href="#endpoints">Endpoints da API</a> -
</p>

## Sobre o Projeto

Projeto feito com Django e Django REST Framework, é uma API para gerenciamento pessoal de notas, permitindo que usuários criem, visualizem, editem e excluam suas anotações com privacidade e segurança.
O controle de acesso é feito com tokens para validações de usúarios, com isso temos segurança para usar as anotações da forma que desejar.

## Funcionalidades

### Usuários
* **Cadastrar de Novos Usuários:** Criação de usuários é feita nome de usuário, email, senha, e campos opcionais de primeiro e segundo nome.
* **Segurança com token:** Login com token gerado durante o cadastro.

### Notas
* **Criar de Notas:** Usuários autenticados podem criar novas notas.
* **Listar de Notas:** Os usuários logados podem ver somente as suas própias notas.
* **Update Notas:** É possível editar um titulo e descrição da nota, e quando isso é feito um selo com a data da atualização é adicionado.
* **Excluir Notas:** Remover notas existentes.
* **Validações de notas:**
    * Título deve ter no mínimo 3 palavras.
    * Titulo e descrição não podem ser iguais
    * Dia da atualização na nota


## Tecnologias

* **Django 5.2.7:** 
* **Django REST Framework 3.x:** 
* **Python 3.12.4:** 
* **SQLite3:**

## Executar

### 1. Clonar o Repositório

```bash
git clone [https://github.com/marinaldosilva/notas.git]
```

### 2. Criar um ambiente virtual venv

```bash
python -m venv venv
para ativar -> venv/bin/activate

```

### 3. Instalar libs do projeto

Instale o arquivo `requirements.txt` para instalar todas as libs.

```bash
pip install -r requirements.txt
```

### 4. Banco de Dados

Utilizamos o banco padrão que se chama sqlite3.
```bash
python manage.py makemigrations Users Notas 
python manage.py migrate                   
```

### 5. Criar um Superusuário 

para acessar o Django `/admin/` crie um superuser:

```bash
python manage.py createsuperuser
```

### 6. Rodar o servidor do projeto

```bash
python manage.py runserver
```

O endereço será `http://127.0.0.1:8000/` é padrão do Django.

## Endpoints


### Autenticação

#### 1. Criação de usuário com Token

* **URL:** `/api/v1/user/cadastro/`
* **Método:** `POST`
* **Autenticação:** Nenhuma.
* **Descrição:** Cria o usuário e gera o token.


```http
POST http://127.0.0.1:8000/api/v1/user/cadastro/

{
    "username": "user",
    "password": "senha"
}
```

```json
{
	"user_id": 1,
	"username": "user",
	"email": "user@hotmail.com",
	"token": "5826ac3ff422080e5ce353cddf5bc8a7f39efbd5"
}
```

---


### Notas

#### 1. Listar Todas as Notas do dono

* **URL:** `/api/v1/notas/listar/`
* **Método:** `GET`
* **Autenticação:** Token.
* **Descrição:** Lista todas as notas criadas pelo usuário.


```
GET http://127.0.0.1:8000//api/v1/notas/listar/
```


```json
{
    "result": [
        {
            "id": 1,
			"dono": "Armani42",
			"titulo": "Product Security Supervisor",
			"descricao": null,
			"data_criacao": "2025-10-29T19:35:37.468916Z",
			"status": 1
        },
        {
            "id": 2,
			"dono": "Armani42",
			"titulo": "Bash tack bluer",
			"descricao": "Serrana Pastosa mel",
			"data_criacao": "2025-10-29T19:35:37.468916Z",
			"status": 1
        }
    ]
}
```

#### 2. Criar Nova Nota

* **URL:** `/api/v1/notas/criar/`
* **Método:** `POST`
* **Autenticação:** Token.
* **Descrição:** Cria uma nova nota.


```http
POST http://127.0.0.1:8000/api/v1/notas/criar/

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
        "descricao": "Passar no mercado antes de voltar pra casa.",
    }
}
```

#### 3. Detalhes de uma Nota Específica

* **URL:** `/api/v1/notas/listar/<int:pk>/`
* **Método:** `GET`
* **Autenticação:** Token.
* **Descrição:** Mostra uma nota especifica

```http
POST http://127.0.0.1:8000/api/v1/notas/listar/
```


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

#### 4. Atualizar uma Nota Específica

* **URL:** `/api/v1/notas/editar/<int:id>/`
* **Método:** `PUT`
* **Autenticação:** Token
* **Descrição:** Atualizar valores da nota.


```http
PUT http://127.0.0.1:8000/api/v1/notas/editar/2/

{
    {
	"titulo":"Robson de valerio",
	"descricao":"boy de valerio",
	"status": 1
    }
}
```


```json
{
    {
	"id": 2,
	"dono": "Armani42",
	"titulo": "Robson De Valerio - Atualizado em 30/10/25",
	"descricao": "boy de valerio",
	"data_criacao": "2025-10-29T19:36:31.958403Z",
	"status": 1
}
}
```

#### 5. Deletar uma Nota Específica

* **URL:** `/notas/<int:pk>/`
* **Método:** `DELETE`
* **Autenticação:** Token (`IsAuthenticated`, `IsOwner`).
* **Descrição:** Remove uma nota existente do usuário autenticado.

**Exemplo de Request:**

```http
DELETE http://127.0.0.1:8000/api/v1/notas/deletar/3/
```

(Sem corpo de resposta)

