## Motivação de criação do projeto

Projeto tem como principal objetivo por em pratica os conceitos aprendidos durante os cursos realizados e pesquisas online nas docs e web.

## Motivos da escolha das funcionalidade

### Users
* As funcionalidades de user foram feitas para que o processo de criação do user fosse feito de forma simples e simplificada. No user temos somente uma rota de acesso livre a todos os usuários (AnonymousUser) 
```http
http://127.0.0.1:8000/api/v1/user/cadastro/
```

Esse é a única rota de user implementada, os demais acessos seram somente via admin.

### Notas
* Para evitar titulos extremamentes curtos tem um limite minimo de palvras.
* O titulo não pode ser igual a descrição da atividade.
* Toda alteração ai receber uma flag de data da atualização no titulo.