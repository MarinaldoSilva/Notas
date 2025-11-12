# Documentação do Projeto Notas

## Visão Geral

`Notas` é uma API REST feita com Django e Django REST Framework para gerenciamento de anotações pessoais. Com nosso foco em segurança(usamos JWT) e notificações por e-mail quando criamos novas notas.

## Conteúdo do Projeto

- Overview por que do projeto.
- Tecnologias e libs utilizadas
- Estrutura do projeto
- Endpoints
- Serialização
- Notificações por e-mail
- Executar o projeto
- Próximos passos

## Tecnologias e libs utilizadas

Algumas das libs utilizdas:

Python
Django 5.2
Django REST Framework
djangorestframework-simplejwt (JWT)
drf-spectacular
dotenv
psycopg2

As demais libs estão no arquivo `requirements.txt`.

## Estrutura do projeto

`users` — model de custom user.
endpoints para cadastro/atualização.

- `authentication` — Contém as responsabilidades signup, signin, signout com tokens de acesso.

* `notas` — model `Notas` que contém os dono, titulo, descricao entre outros, também tem os serializers, views e utils onde temas requisições de E-mail.

## Endpoints principais

Obs.: todas as rotas de `notas` exigem autenticação JWT (exceto as públicas especificadas).

- Autenticação / Usuário

  - POST `/api/v1/auth/signup/` — cria usuário e tokens (access, refresh)
  - POST `/api/v1/auth/signin/` — autenticação por email e senha com o retorno de tokens
  - POST `/api/v1/auth/signout/` — invalida o refresh token
  - GET `/api/v1/user/` — retorna os dados do usuário autenticado
  - PATCH `/api/v1/user/<pk>/` — atualiza usuário.

- Notas
  - GET `/api/v1/notas/listar/` — lista todas as notas do user logado
  - GET `/api/v1/notas/listar/<pk>/` — Retorna um user especifico
  - POST `/api/v1/notas/criar/` — criação de notas e envio de E-amil
  - PATCH `/api/v1/notas/editar/<pk>/` — atualização parcial de uma nota
  - DELETE `/api/v1/notas/deletar/<pk>/` — Apaga uma nota especifica

## Serializer

É responsável por transformar o Json em Python na serialização dos dados e faz o oposto na devolução para a view renderizado em JSON. Recebe todos os campos listados no `fields` para obter o valor na requisição, alguns campos como senha são omitidos no retorno, como por exemplo o `password`.

## Notificações por e-mail

Em nosso `notas/utils.py`

Temos o `form_email que envia um e-mail HTML ao usuário quando uma anotação é criada, o celery faz isso para nós em 2º plano.

Comportamento:

- Durante a criação da nota é disparado um e-mail com o `titulo_nota` para o destinatario que foi cadastrado durante a criação do usuário.
- Usa `settings.DEFAULT_FROM_EMAIL` como remetente remetente padrão do envio de E-mail e o Celery faz a gestão dos envios em segundo plano.

## Executar o projeto

1. Crie um virtualenv

```bash
py -m venv venv
```

```bash
\venv\Scripts\Activate
```

instale dependências:

```bash
install -r requirements.txt
```

2. Com o arquivo `.env.local` como exemplo, criei e configure o seu banco e configurações de e-mail.

3. Rode migrations e crie um superuser:

```bash
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

4. Swagger
   Exibi de forma amigavel ao usuário o sistema em si

```bash
http://127.0.0.1:8000/api/schema/swagger-ui/#/
```

## Boas práticas & performance

- Evitar N+1: usar `select_related('dono')` / `prefetch_related` ao construir querysets para serialização em massa.
- Tornar o envio de e-mails assíncrono (Celery, Django-Q, BackgroundTasks) para melhorar latência da API.
- Usar logs estruturados em vez de `print`.
- Adicionar testes unitários para serializers e views (happy-path + alguns erros).

## Testes

- Existem testes de criação, edição e exclusão de usuários e notas, em cada app tem o seu arquivos de estes.

Para testar usamos:

```py
test -s -v
```

## Próximos passos

- Disparo de E-mail com o Celery
- Configuração do paginação e filtros na exibição das notas.
- Ajustar e refinar a documentação para melhorar os exemplos.
