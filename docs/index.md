# Documentação do Projeto Notas

## Visão Geral do Projeto

O projeto Notas é uma API REST desenvolvida em Django que permite aos usuários criar e gerenciar anotações pessoais de forma segura. O sistema implementa autenticação JWT e oferece funcionalidades robustas de gerenciamento de notas.

## Sistema de Notificações por E-mail

O sistema inclui um serviço de notificações por e-mail implementado no módulo `utils.py`. Este serviço é responsável por enviar emails automáticos quando novas notas são criadas.

### Implementação do Serviço de E-mail (`utils.py`)

```python
def form_email(user_email: str, titulo_nota: str):
    """
    Envia um e-mail de confirmação quando uma nova nota é cadastrada no sistema.
    
    Parâmetros:
    - user_email: E-mail do destinatário
    - titulo_nota: Título da nota criada
    """
```

### Características do Sistema de E-mail

1. **Template Personalizado**
   - Utiliza template HTML localizado em `templates/email/form_email.html`
   - Suporta formatação rica e personalização do conteúdo
   - Dados dinâmicos incluem e-mail do usuário e título da nota

2. **Configuração**
   - Utiliza configurações do Django settings
   - Remetente configurável via `settings.DEFAULT_FROM_EMAIL`
   - Suporte a múltiplos destinatários

3. **Tratamento de Erros**
   - Sistema robusto de tratamento de exceções
   - Logs detalhados de sucesso e falha
   - Mensagens informativas no console

4. **Funcionalidades**
   - Assunto personalizado com o título da nota
   - Mensagem em formato HTML
   - Confirmação de envio no console
   - Tratamento de falhas silenciosas desativado para melhor debugging

### Exemplo de Uso do Sistema de E-mail

```python
# Exemplo de chamada da função
form_email("usuario@exemplo.com", "Minha Nova Nota")

# Saída de sucesso no console
"Enviado com sucesso!"
"E-mail de criação de nota enviado para usuario@exemplo.com com título 'Minha Nova Nota'."
```

### Integração com o Django

- Utiliza o sistema de templates do Django
- Aproveita as configurações de e-mail do projeto
- Integrado com o modelo de notas
- Chamado automaticamente após a criação de uma nova nota

## Tecnologias Utilizadas

- Django 5.2.7
- Django REST Framework 3.16.1
- JWT Authentication (djangorestframework_simplejwt 5.5.1)
- Swagger/OpenAPI (drf-spectacular 0.28.0)
- PostgreSQL (psycopg2 2.9.11)
- Python-dotenv 1.2.1
- CORS Headers 4.9.0

## Motivação do Projeto

O projeto tem como principal objetivo colocar em prática os conceitos aprendidos durante os cursos realizados e pesquisas online nas documentações e web, implementando boas práticas de desenvolvimento e padrões de segurança.

## Funcionalidades e Implementações

### Users
As funcionalidades de user foram feitas para que o processo de criação do user fosse feito de forma simples e simplificada. No user temos somente uma rota de acesso livre a todos os usuários (AnonymousUser) 
```http
http://127.0.0.1:8000/api/v1/user/cadastro/
```

```py
class UserCreateAPIView(APIView):

    permission_classes = [AllowAny]

```

Esse é a única rota de user implementada, os demais acessos seram somente via admin, e nessa rota a permissão é livre.

### Token JWT
A utilização do token jwt se dar por motivos de seurança e geração do tokens com prazos de validade curtos, assim é possível trabalhar melhor com logins e logouts.
Temos tem rotas:

Obter Token access e refresh

```http
http://127.0.0.1:8000/api/token/
```
```json
	{
	"username":"user",
	"password":"senha"
}
```
E gera uma resposta:

```json
{
	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
	"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Atualização de token(refresh):

```http
http://127.0.0.1:8000/api/token/refresh
```
Passe seu token access gerado
```json
"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

e receba um novo token nesse mesmo modelo de resposta

Desabilitar um token e evitar que seja reutilizado novamente

```http
http://127.0.0.1:8000/api/token/blacklist/
```
passe seu token

```json
{
	"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

e a resposta é

```json
{
	"detail": "Token has wrong type",
	"code": "token_not_valid"
}
```

### Notas
As notas (anotações) dos usuários foram projetadas para serem seguras e com base nisso necessitam de autenticação, é necessário um user com token para acessar as views. No serializer tem três campos de validações, onde tem as validações por `campo` e `validated_data`, eles são:


* Para evitar titulos extremamentes curtos tem um limite minimo de palvras.

```python
def validate_titulo(self, value):
        min_palavras = 3
        if len(value.split()) < min_palavras:
            raise serializers.ValidationError(f"O titulo deve ter pelo menos {min_palavras} palavras")
        return value.title()
```

* O titulo não pode ser igual a descrição da atividade.

```python
def validate(self, data):
        titulo = data['titulo']
        descricao = data['descricao']

        if titulo and descricao:
            if titulo.strip().lower() == descricao.strip().lower():
                raise serializers.ValidationError("O titulo não pode ser igual a descrição da atividade.")
            return data
```

* Toda alteração ai receber uma flag de data da atualização no titulo.


```python
def update(self, instance, validated_data):
        if 'titulo' in validated_data and instance.titulo != validated_data['titulo']:
            data_update_title = datetime.now().strftime("%d/%m/%y")
            validated_data['titulo'] = f"{validated_data['titulo']} - Atualizado em {data_update_title}"
            return super().update(instance, validated_data)
        return instance
```

São funções personalizadas para dar mais robustez no processo de criação das notas.

Temos 4 rotas:

Criação de anotações:

```http
http://127.0.0.1:8000/api/v1/notas/criar/
```

```json
{
	"titulo":"teste,teste teste",
	"descricao":"testetesteteste",
	"status":2
}
```
Criação de listar:

```http
http://127.0.0.1:8000/api/v1/notas/listar/

```
```json
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
			"titulo": "Robson De Valerio - Atualizado em 30/10/25",
			"descricao": "boy de valerio",
			"data_criacao": "2025-10-29T19:36:31.958403Z",
			"status": 1
		}
```

 e listar por PK/ID:

 ```http
http://127.0.0.1:8000/api/v1/notas/listar/<int:pk>
```
```json
{
			"id": 1,
			"dono": "Armani42",
			"titulo": "Product Security Supervisor",
			"descricao": null,
			"data_criacao": "2025-10-29T19:35:37.468916Z",
			"status": 1
		}
```

Editar:

```http
http://127.0.0.1:8000/api/v1/notas/editar/<int:pk>
```

```json
{
	"titulo":"Robson de valerio",
	"descricao":"boy de valerio",
	"status": 1
}
```

```json
{
	"id": 2,
	"dono": "Armani42",
	"titulo": "Robson De Valerio - Atualizado em 30/10/25",
	"descricao": "boy de valerio",
	"data_criacao": "2025-10-29T19:36:31.958403Z",
	"status": 1
}
```

Excluir:

```http
http://127.0.0.1:8000/api/v1/notas/deletar/<int:pk>
```
```json
204 No Content
```
Esses são exemplos de entrada e saídas de rotas do sistema.

O sistema em si é simples, mas funcional e fiel ao que se propôe, tem camadas de segurança, é robusta no que se propôe e totalmente escalavel.

### Documentação com Swagger

Foram mapeadas as rotas para facilitar a visualização, configurações pendentes de finalização.

```http
http://127.0.0.1:8000/api/schema/swagger-ui/#/
```

vai retornar uma lista com todas as rotas do sistema.