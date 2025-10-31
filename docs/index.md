## Motivação de criação do projeto

Projeto tem como principal objetivo por em pratica os conceitos aprendidos durante os cursos realizados e pesquisas online nas docs e web.

## Motivos da escolha das funcionalidade

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